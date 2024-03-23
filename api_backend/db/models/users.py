import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column
from api_backend.db.models.base import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(sqlalchemy.BigInteger, primary_key=True)
    username: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    date_registered: Mapped[str]
