import random
import asyncio
import logging

from sqlalchemy import update

from app.broker import broker, payments_queue, payments_exchange
from app.database import AsyncSessionLocal
from app.models import PaymentModel
from app.models.payment import PaymentStatus

logger = logging.getLogger(__name__)


@broker.subscriber(payments_queue, exchange=payments_exchange)
async def process_payment_message(data: dict):
    outbox_id = data.get("outbox_id")
    payment_id = int(data.get("payment_id"))
    logger.info(f"Payment: payment_id={payment_id}, outbox_id={outbox_id}")

    try:
        await asyncio.sleep(2.5)
        is_success = random.random() < 0.90

        if not is_success:
            raise RuntimeError("Reject the transaction")

        async with AsyncSessionLocal() as session:
            payment = update(PaymentModel).where(PaymentModel.id == payment_id).values(status=PaymentStatus.SUCCESS)
            await session.execute(payment)
            await session.commit()

        logger.info(f"Payment {payment_id} succeded")

    except Exception as e:
        logger.error(f"Error with payment {payment_id}: {e}")

        raise e
