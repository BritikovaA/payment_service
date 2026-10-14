from fastapi import FastAPI

app = FastAPI(title="Payment Service")

@app.get("/")
async def root():
    return {"status": "ok","message": "Service available"}