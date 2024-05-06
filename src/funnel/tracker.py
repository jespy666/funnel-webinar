from collections.abc import Sequence
from typing import Dict

from datetime import datetime, timedelta

from src.database.models import User
from src.database.crud import CRUD

from config import settings


class MessageFunnelTracker(CRUD):

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    async def get_stage1_users(users: Sequence[User]) -> Dict[int, str] | None:
        target: timedelta = timedelta(minutes=settings.STAGE_1)
        return {
            user.id: settings.MESSAGE1 for user in users
            if user.status == 'alive'
            and user.current_stage == 0
            and (user.created_at + target) < datetime.utcnow()
        }

    @staticmethod
    async def get_stage2_users(users: Sequence[User]) -> Dict[int, str] | None:
        target: timedelta = timedelta(minutes=settings.STAGE_2)
        return {
            user.id: settings.MESSAGE2 for user in users
            if user.status == 'alive'
            and user.current_stage == 1
            and (user.last_message_sent + target) < datetime.utcnow()
        }

    @staticmethod
    async def get_stage3_users(users: Sequence[User]) -> Dict[int, str] | None:
        target: timedelta = timedelta(minutes=settings.STAGE_3)
        alive_users = {
            user.id: settings.MESSAGE3 for user in users
            if user.status == 'alive'
            and user.current_stage == 2
            and (user.last_message_sent + target) < datetime.utcnow()
        }
        finished_users = {
            user.id: settings.MESSAGE3 for user in users
            if user.status == 'finished'
            and user.current_stage == 2
            and (user.last_message_sent + target) < datetime.utcnow()
        }
        if finished_users:
            alive_users.update(finished_users)
        return alive_users

    async def get_ready_to_send_users(self) -> Dict[int, str]:
        users: Sequence[User] = await super().get_users_by_status(
            ['alive', 'finished']
        )
        stage1: Dict[int, str] | None = await self.get_stage1_users(users)
        stage2: Dict[int, str] | None = await self.get_stage2_users(users)
        stage3: Dict[int, str] | None = await self.get_stage3_users(users)
        return {**stage1, **stage2, **stage3}
