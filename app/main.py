from fastapi import FastAPI
from app.routers.payments import router as payments_router

app = FastAPI(title="Payment Service")

app.include_router(payments_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"status": "ok","message": "Service available"}