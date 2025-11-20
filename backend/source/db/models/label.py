from .base import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Label(Base):
    __tablename__ = "labels"
    name: Mapped[str] = mapped_column(String(length=260))
