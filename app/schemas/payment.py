from datetime import datetime
from decimal import Decimal
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from app.models.payment import CurrencyEnum, PaymentStatus


class PaymentCreate(BaseModel):
    amount: Decimal = Field(..., gt=0)
    currency: CurrencyEnum
    description: Optional[str] = Field(None, max_length=255)
    webhook_url: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class PaymentResponse(BaseModel):
    id: int
    amount: Decimal
    currency: CurrencyEnum
    description: Optional[str] = None
    status: PaymentStatus
    webhook_url: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = Field(default=None, validation_alias="payment_metadata")
    created_at: datetime

    class Config:
        from_attributes = True
