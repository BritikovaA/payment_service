import enum
from sqlalchemy import Column, Integer, DateTime, Enum, func, ForeignKey
from app.database import Base


class OutboxStatus(str, enum.Enum):
    PENDING = "pending"
    SUCCESS = "processed"


class OutboxModel(Base):
    __tablename__ = "outbox"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    payment_id = Column(Integer, ForeignKey("payments.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(OutboxStatus), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
