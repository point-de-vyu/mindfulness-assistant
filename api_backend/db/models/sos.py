from sqlalchemy import BigInteger, JSON, VARCHAR, TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api_backend.db.models.base import Base
from typing import Any, List
from sqlalchemy import ForeignKey


class SosSituation(Base):
    __tablename__ = "sos_situations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(length=50))

    rituals: Mapped[List["SosRitual"]] = relationship()


class SosCategory(Base):
    __tablename__ = "sos_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(length=30))

    rituals: Mapped[List["SosRitual"]] = relationship()


class SosRitual(Base):
    __tablename__ = "sos_rituals"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("sos_categories.id", ondelete="CASCADE")
    )
    situation_id: Mapped[int] = mapped_column(
        ForeignKey("sos_situations.id", ondelete="CASCADE")
    )
    title: Mapped[str] = mapped_column(TEXT)
    description: Mapped[str] = mapped_column(TEXT)
    url: Mapped[str] = mapped_column(TEXT)
    tags: Mapped[dict[str, Any]] = mapped_column(JSON)

    added_rituals: Mapped[List["UserRitual"]] = relationship()


class SosDefaultRitualId(Base):
    __tablename__ = "sos_rituals_default_ids"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)


class UserRitual(Base):
    __tablename__ = "user_sos_ritual"

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    ritual_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("sos_rituals.id", ondelete="CASCADE"), primary_key=True
    )
