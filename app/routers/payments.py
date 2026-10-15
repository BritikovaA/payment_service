from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.payment import PaymentModel, PaymentStatus
from app.models.outbox import OutboxModel, OutboxStatus
from app.schemas.payment import PaymentCreate, PaymentResponse, PaymentBaseResponse
from app.core.deps import verify_api_key, get_idempotency_key

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/", response_model=PaymentBaseResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_payment(
        payment: PaymentCreate,
        db: AsyncSession = Depends(get_db),
        api_key: str = Depends(verify_api_key),
        idempotency_key: str = Depends(get_idempotency_key), ):
    slct_payment = select(PaymentModel).where(PaymentModel.idempotency_key == idempotency_key)
    result = await db.execute(slct_payment)
    existing_payment = result.scalar_one_or_none()

    if existing_payment:
        return existing_payment

    db_payment = PaymentModel(
        **payment.model_dump(),
        idempotency_key=idempotency_key,
        status=PaymentStatus.PENDING,
    )
    db.add(db_payment)
    await db.flush()

    db_outbox = OutboxModel(
        payment_id=db_payment.id,
        status=OutboxStatus.PENDING,
    )
    db.add(db_outbox)

    await db.commit()
    await db.refresh(db_payment)

    return db_payment


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(payment_id: int,
                      db: AsyncSession = Depends(get_db),
                      api_key: str = Depends(verify_api_key), ):
    payment = await db.get(PaymentModel, payment_id)

    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )

    return payment

