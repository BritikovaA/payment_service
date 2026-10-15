import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers.payments import router as payments_router
from app.broker import broker, payments_exchange, payments_queue
from app.outbox_worker import process_outbox_messages
import logging
import app.consumer

logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

@asynccontextmanager
async def lifespan(_: FastAPI):
    await broker.connect()
    await broker.declare_exchange(payments_exchange)
    await broker.declare_queue(payments_queue)
    await broker.start()
    worker_task = asyncio.create_task(process_outbox_messages())

    yield

    worker_task.cancel()
    await broker.stop()


app = FastAPI(title="Payment Service", lifespan=lifespan)

app.include_router(payments_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"status": "ok", "message": "Service available"}
