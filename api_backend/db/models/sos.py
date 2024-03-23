import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column
from api_backend.db.models.base import Base
from typing import Any
from sqlalchemy import ForeignKey


class SosSituation(Base):
    __tablename__ = "sos_situations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class SosCategory(Base):
    __tablename__ = "sos_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class SosRitual(Base):
    __tablename__ = "sos_rituals"

    id: Mapped[int] = mapped_column(sqlalchemy.BigInteger, primary_key=True)
    # FK to sos_categories.id
    category_id: Mapped[int]
    # FK to sos_situations.id
    situation_id: Mapped[int]
    title: Mapped[str]
    description: Mapped[str]
    url: Mapped[str]
    tags: Mapped[dict[str, Any]] = mapped_column(sqlalchemy.JSON)


class SosDefaultRitualId(Base):
    __tablename__ = "sos_rituals_default_ids"

    id: Mapped[int] = mapped_column(sqlalchemy.BigInteger, primary_key=True)


class UserRitual(Base):
    __tablename__ = "user_sos_ritual"
    # FK to users.id
    user_id: Mapped[int] = mapped_column(sqlalchemy.BigInteger, primary_key=True)
    # FK to sos_rituals.id
    ritual_id: Mapped[int] = mapped_column(sqlalchemy.BigInteger, primary_key=True)
