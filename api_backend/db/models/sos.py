import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column
from api_backend.db.models.base import Base


class SosSituations(Base):
    __tablename__ = "sos_situations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class SosCategories(Base):
    __tablename__ = "sos_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class SosDefaultRitualIds(Base):
    __tablename__ = "sos_rituals_default_ids"

    id: Mapped[int] = mapped_column(sqlalchemy.BigInteger, primary_key=True)


class UserRitual(Base):
    __tablename__ = "user_sos_ritual"

    user_id: Mapped[int] = mapped_column(sqlalchemy.BigInteger, primary_key=True)
    ritual_id: Mapped[int] = mapped_column(sqlalchemy.BigInteger, primary_key=True)