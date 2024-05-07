import asyncio
import time

from datetime import datetime

from typing import Dict

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import RPCError, FloodWait

from src.database.models import User
from src.database.crud import CRUD
from src.funnel import MessageFunnelTracker, StageControl

from loguru import logger

from config import settings


app = Client(
    name=settings.TG_CONFIG.name,
    api_id=settings.TG_CONFIG.api_id,
    api_hash=settings.TG_CONFIG.api_hash
)


@app.on_message(filters.private & filters.text)
async def handle_msg(_, msg: Message) -> None:
    outgoing_msg = msg.outgoing
    # check type of message (incoming / outgoing)
    user_id: int = msg.chat.id if outgoing_msg else msg.from_user.id
    text: list = msg.text.lower().split()
    user: User | None = await CRUD().get_user(user_id)
    now = datetime.utcnow()
    # create new user if not exist
    if not user:
        await CRUD().create_user(user_id)
        logger.info('Новый пользователь в воронке: {}', user_id)
    if outgoing_msg:
        current_stage: int = user.current_stage
        if any(word in text for word in settings.CANCEL_TRIGGERS):
            if 1 <= current_stage < 3:
                next_stage = current_stage + 1
                logger.warning('Триггер на следующий этап: {}', user_id)
                await CRUD().update_user(
                    user_id,
                    current_stage=next_stage,
                    last_message_sent=now,
                    trigger=True,
                )
        if any(word in text for word in settings.FINISH_TRIGGERS):
            logger.warning('Найден завершающий триггер: {}', user_id)
            await CRUD().update_user(
                user_id,
                current_stage=3,
                status='finished',
                status_updated_at=now,
                last_message_sent=now,
            )
        logger.info('Сообщение отправлено пользователю: {}', user_id)
    else:
        logger.info('Сообщение от пользователя: {}', user_id)


async def funnel_task() -> None:
    while True:
        tracker = MessageFunnelTracker()
        # fetch ready to accept message users by timing
        ready_users: Dict[int, str] = await tracker.get_ready_to_send_users()
        for user_id, message in ready_users.items():
            try:
                await app.send_message(user_id, message)
                logger.success(
                    'Сообщение воронки успешно отправлено пользователю: {}',
                    user_id,
                )
                # set up user for next stage
                await StageControl(user_id).setup_by_stage(datetime.utcnow())
            except FloodWait as e:
                logger.warning(
                    'Превышен лимит сообщений {}\nОжидание...',
                    e,
                )
                time.sleep(e.ID)
            except RPCError as e:
                logger.critical(
                    'Произошла ошибка при отправке сообщения: {}',
                    e,
                )
                await CRUD().update_user(
                    user_id,
                    status='dead',
                    status_updated_at=datetime.utcnow(),
                )
        # set loop delay
        await asyncio.sleep(settings.LOOP_DELAY)


async def run():
    # run msg handler and while true task as parallel
    await asyncio.gather(app.start(), funnel_task())


if __name__ == '__main__':
    try:
        logger.success('Юзербот успешно запущен')
        asyncio.get_event_loop().run_until_complete(run())
    finally:
        logger.critical('Юзербот остановлен')
