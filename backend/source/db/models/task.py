from .base import Base
from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column


class Task(Base):
    __tablename__ = "tasks"
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status_id: Mapped[int] = mapped_column(ForeignKey("statuses.id"))
    priority_id: Mapped[int] = mapped_column(ForeignKey("priorities.id"))
    label_id: Mapped[int] = mapped_column(ForeignKey("labels.id"))
    
    created_at: Mapped[datetime] = mapped_column(DateTime())
    deadline: Mapped[datetime] = mapped_column(DateTime())
    
    description: Mapped[str] = mapped_column(Text())
    