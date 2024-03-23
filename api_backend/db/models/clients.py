import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column
from api_backend.db.models.base import Base


class ClientTypes(Base):
    __tablename__ = "client_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class Clients(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    # FK to client_types.id
    client_type_id: Mapped[int]
    token: Mapped[str] = mapped_column(sqlalchemy.VARCHAR(length=64))


class ClientsUsers(Base):
    __tablename__ = "clients_users"

    client_id: Mapped[int] = mapped_column(primary_key=True)
    user_id_from_client: Mapped[int] = mapped_column(primary_key=True)
    # FK to user.id (change? to being here)
    user_id: Mapped[int] = mapped_column(sqlalchemy.BigInteger)
