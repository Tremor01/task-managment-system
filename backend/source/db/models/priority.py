from .base import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Priority(Base):
    __tablename__ = "priorities"
    name: Mapped[str] = mapped_column(String(length=260))
