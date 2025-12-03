from .base import Base
from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column


class Task(Base):
    __tablename__ = "tasks"
    
    status_id: Mapped[int | None] = mapped_column(ForeignKey("statuses.id"), nullable=True)
    priority_id: Mapped[int | None] = mapped_column(ForeignKey("priorities.id"), nullable=True)
    label_id: Mapped[int | None] = mapped_column(ForeignKey("labels.id"), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime())
    deadline: Mapped[datetime | None] = mapped_column(DateTime(), nullable=True)
    
    description: Mapped[str] = mapped_column(Text())