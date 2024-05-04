from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    declared_attr
)
from sqlalchemy.dialects.sqlite import TIMESTAMP
from sqlalchemy import func, Enum
from datetime import datetime


class Base(DeclarativeBase):

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        unique=False,
        server_default=func.now(),
    )
    status: Mapped[str] = mapped_column(
        Enum('alive', 'dead', 'finished'),
        nullable=False,
        unique=False,
        default='alive',
    )
    status_updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        unique=False,
        onupdate=func.now(),
    )

    def __repr__(self):
        return str(self)
