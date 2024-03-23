from sqlalchemy import Integer, BigInteger, VARCHAR, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api_backend.db.models.base import Base
from api_backend.db.models.users import User


class ClientType(Base):
    __tablename__ = "client_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(length=30))


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("client_types.id", ondelete="CASCADE")
    )
    token: Mapped[str] = mapped_column(VARCHAR(length=64))

    client_type = relationship(ClientType)


class ClientsUsers(Base):
    __tablename__ = "clients_users"

    client_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("clients.id", ondelete="CASCADE"), primary_key=True
    )
    user_id_from_client: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE")
    )

    user = relationship(User)
    client = relationship(Client)
