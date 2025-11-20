from .base import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(length=260))
    hash_password: Mapped[str] = mapped_column(String(length=260))
    username: Mapped[str] = mapped_column(String(length=30))
