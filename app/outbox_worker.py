import asyncio
import logging
from sqlalchemy import select, update

from app.database import AsyncSessionLocal
from app.models.outbox import OutboxModel, OutboxStatus
from app.broker import broker, payments_exchange

logger = logging.getLogger(__name__)


async def process_outbox_messages():
    await asyncio.sleep(2)

    while True:
        try:
            async with AsyncSessionLocal() as session:
                payments = (
                    select(OutboxModel)
                    .where(OutboxModel.status == OutboxStatus.PENDING)
                    .limit(5)
                    )
                result = await session.execute(payments)
                outbox_elements = result.scalars().all()

                if not outbox_elements:
                    await asyncio.sleep(2)
                    continue

                for element in outbox_elements:
                    try:
                        await broker.publish(
                            {"outbox_id": str(element.id), "payment_id": str(element.payment_id)},
                            exchange=payments_exchange,
                            routing_key="payments.new"
                        )

                        update_stmt = (
                            update(OutboxModel)
                            .where(OutboxModel.id == element.id)
                            .values(status=OutboxStatus.SUCCESS)
                        )
                        await session.execute(update_stmt)
                        await session.commit()

                        logger.info(f"Outbox {element.id} sent")

                    except Exception as pub_error:
                        await session.rollback()
                        logger.error(f"Failed the outbox {element.id}: {pub_error}")
        except Exception as e:
            logger.error(f"Error in worker loop: {e}")

        await asyncio.sleep(5)