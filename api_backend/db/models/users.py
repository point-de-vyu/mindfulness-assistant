from sqlalchemy import BigInteger, TEXT, DATE
from sqlalchemy.orm import Mapped, mapped_column
from api_backend.db.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(TEXT)
    first_name: Mapped[str] = mapped_column(TEXT)
    last_name: Mapped[str] = mapped_column(TEXT)
    date_registered: Mapped[str] = mapped_column(DATE)
