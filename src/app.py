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
    if outgoing_msg:
        user_id: int = msg.chat.id
        logger.info('Сообщение отправлено пользователю: {}', user_id)
    else:
        user_id: int = msg.from_user.id
        logger.info('Новое сообщение от пользователя: {}', user_id)
    user: User | None = await CRUD().get_user(user_id)
    # create new user if not exist
    if not user:
        user: User = await CRUD().create_user(user_id)
        logger.info('Добавлен новый пользователь: {}', user_id)
    msg_text: str = msg.text
    # check for triggers in message
    if any(word in msg_text.lower().split() for word in settings.TRIGGERS):
        # check if user already get first stage funnel message
        if 1 <= user.current_stage < 3:
            now = datetime.utcnow()
            if outgoing_msg:
                logger.warning('Найден триггер в сообщении ассистента!')
            else:
                logger.warning('Найден триггер в сообщении пользователя!')
            await CRUD().update_user(
                user_id,
                status='finished',
                current_stage=2,
                last_message_sent=now,
                status_updated_at=now,
            )
            logger.warning('Воронка для пользователя: {} завершена!', user_id)


async def funnel_task() -> None:
    while True:
        tracker = MessageFunnelTracker()
        # fetch ready to accept message users by timing
        ready_users: Dict[int, str] = await tracker.get_ready_to_send_users()
        for user_id, message in ready_users.items():
            try:
                await app.send_message(user_id, message)
                logger.success(
                    'Сообщение было успешно отправлено пользователю: {}',
                    user_id,
                )
                # set up user for next stage
                await StageControl(user_id).setup_by_stage(datetime.utcnow())
                logger.success('STAGE UPGRADED')
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
    try:
        logger.success('Юзербот успешно запущен')
        # run msg handler and while true task as parallel
        await asyncio.gather(app.start(), funnel_task())
    finally:
        logger.warning('Юзербот остановлен')


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(run())
