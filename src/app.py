from pyrogram import Client, filters

from src.database.crud import CRUD
from config import TG_CONFIG


app = Client('test', api_id=TG_CONFIG.api_id, api_hash=TG_CONFIG.api_hash)


# TEST
@app.on_message(filters.text & filters.private)
async def handle_msg(_, message) -> None:
    user_id: int = message.from_user.id
    user = await CRUD().get_user(user_id)
    if not user:
        user = await CRUD().create_user(user_id)
        await message.reply(f'{user.id} создан {user.created_at} статус {user.status}')


if __name__ == '__main__':
    app.run()
