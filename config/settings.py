from pathlib import Path

from dotenv import load_dotenv
import os

from dataclasses import dataclass

from typing import Optional


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


@dataclass
class DBConfig:
    db_type: str
    db_name: str
    db_user: Optional[str] = None
    db_password: Optional[str] = None
    db_host: Optional[str] = None
    db_port: Optional[str] = None

    def get_connection_url(self) -> str:
        match self.db_type:
            case db if db == 'sqlite':
                return f'sqlite+aiosqlite:////{BASE_DIR}/{self.db_name}'
            case db if db == 'postgres':
                return (
                    f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
                    f"@{self.db_host}:{self.db_port}/{self.db_name}"
                )
            case _:
                raise ValueError("Unsupported database type")


@dataclass
class TGConfig:
    name: str
    api_id: int
    api_hash: str


# Config database
DB_CONFIG = DBConfig(
    db_type=os.getenv('DB_TYPE'),
    db_name=os.getenv('DB_NAME'),
    db_user=os.getenv('DB_USER'),
    db_password=os.getenv('DB_PASSWORD'),
    db_host=os.getenv('DB_HOST'),
    db_port=os.getenv('DB_PORT'),
)

# Config Pyrogram client
TG_CONFIG = TGConfig(
    name='Your client name',
    api_id=int(os.getenv('API_ID')),
    api_hash=os.getenv('API_HASH'),
)

# Text in funnel messages
MESSAGE1 = 'Текст 1'
MESSAGE2 = 'Текст 2'
MESSAGE3 = 'Текст 3'

# Triggers for finished funnel
FINISH_TRIGGERS = ['прекрасно', 'ожидать']
# Triggers for next funnel stage
CANCEL_TRIGGERS = ['триггер1']

# Message delay time (in minutes)
STAGE_1 = 6  # 6 minutes by technical task
STAGE_2 = 39  # 39 minutes by technical task
STAGE_3 = 1740  # 1740 minutes by technical task

# While True task loop delay (in seconds)
LOOP_DELAY = 30
