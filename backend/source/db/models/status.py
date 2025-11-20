from .base import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Status(Base):
    __tablename__ = "statuses"
    name: Mapped[str] = mapped_column(String(length=260))
