from datetime import datetime

from src.database.crud import CRUD
from src.database.models import User


class StageControl(CRUD):

    def __init__(self, user_id: int) -> None:
        super().__init__()
        self.user_id = user_id

    async def setup_by_stage(self, now: datetime) -> None:
        user: User = await super().get_user(self.user_id)
        current_stage: int = user.current_stage
        trigger: bool = user.trigger
        fields_to_setup = {'last_message_sent': now}
        match current_stage:
            case s if s == 0:
                next_stage = 1 if not trigger else 2
            case s if s == 1:
                next_stage = 2 if not trigger else 3
            case s if s == 2:
                fields_to_setup['status'] = 'finished'
                fields_to_setup['status_updated_at'] = now
                next_stage = 3
            case _:
                return
        fields_to_setup['current_stage'] = next_stage
        await super().update_user(self.user_id, **fields_to_setup)
