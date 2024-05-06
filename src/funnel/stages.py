from datetime import datetime

from src.database.crud import CRUD
from src.database.models import User


class StageControl(CRUD):

    def __init__(self, user_id: int) -> None:
        super().__init__()
        self.user_id = user_id

    async def get_stage(self) -> int:
        user: User = await super().get_user(self.user_id)
        return user.current_stage

    async def setup_by_stage(self, now: datetime) -> None:
        current_stage: int = await self.get_stage()
        fields_to_setup = {'last_message_sent': now}
        match current_stage:
            case s if s == 0:
                next_stage = 1
            case s if s == 1:
                next_stage = 2
            case s if s == 2:
                fields_to_setup['status'] = 'finished'
                fields_to_setup['status_updated_at'] = now
                next_stage = 3
            case _:
                return
        fields_to_setup['current_stage'] = next_stage
        await super().update_user(self.user_id, **fields_to_setup)
