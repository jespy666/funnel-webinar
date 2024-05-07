from datetime import datetime

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    declared_attr
)
from sqlalchemy import func, Enum, Integer, Boolean

from config import DB_CONFIG

if DB_CONFIG.db_type == 'postgres':
    from sqlalchemy.dialects.postgresql import TIMESTAMP
else:
    from sqlalchemy.dialects.sqlite import TIMESTAMP


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
        unique=False,
        nullable=True,
        default=None,
    )
    last_message_sent: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        unique=False,
        default=datetime.utcnow(),
    )
    current_stage: Mapped[int] = mapped_column(
        Integer,
        unique=False,
        default=0,
    )
    trigger: Mapped[bool] = mapped_column(
        Boolean,
        unique=False,
        default=False,
    )

    def __repr__(self):
        return str(self)
