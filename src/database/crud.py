from collections.abc import Sequence
from typing import List

from sqlalchemy import select, delete, or_, update
from sqlalchemy.ext.asyncio import AsyncSession

from .session import AsyncSessionFactory
from .models import User

from config import DB_CONFIG


class CRUD(AsyncSessionFactory):

    def __init__(self) -> None:
        url = DB_CONFIG.get_connection_url()
        super().__init__(url)

    async def create_user(self, pk: int) -> User:
        user = User(id=pk)
        session: AsyncSession = await super().get_session()
        session.add(user)
        await session.commit()
        await session.close()
        return user

    async def get_user(self, pk: int) -> User | None:
        stmt = select(User).where(User.id == pk)
        session: AsyncSession = await super().get_session()
        user: User | None = await session.scalar(stmt)
        await session.close()
        return user

    async def get_users_by_status(self, statuses: List[str]) -> Sequence[User]:
        stmt = select(User).filter(or_(
            *[User.status == status for status in statuses]
        ))
        session: AsyncSession = await super().get_session()
        result = await session.execute(stmt)
        users: Sequence[User] = result.scalars().all()
        await session.close()
        return users

    async def update_user(self, user_id: int, **kwargs) -> None:
        stmt = update(User).where(User.id == user_id).values(**kwargs)
        session: AsyncSession = await super().get_session()
        await session.execute(stmt)
        await session.commit()
        await session.close()

    async def delete_user(self, pk: int) -> None:
        stmt = delete(User).where(User.id == pk)
        session = await super().get_session()
        await session.execute(stmt)
        await session.commit()
        await session.close()
