import enum
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Enum, JSON, func
from app.database import Base


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    SUCCESS = "succeeded"
    FAILED = "failed"


class CurrencyEnum(str, enum.Enum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"


class PaymentModel(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(Enum(CurrencyEnum), nullable=False)
    description = Column(String(255), nullable=True)
    status = Column(Enum(PaymentStatus), nullable=False)
    payment_metadata = Column("metadata", JSON, nullable=True)
    idempotency_key = Column(String(255), unique=True, index=True, nullable=False)
    webhook_url = Column(String(512), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True),server_default=func.now(), onupdate=func.now(), nullable=False)