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
    api_id: int
    api_hash: str


DB_CONFIG = DBConfig(
    db_type=os.getenv('DB_TYPE'),
    db_name=os.getenv('DB_NAME'),
    db_user=os.getenv('DB_USER'),
    db_password=os.getenv('DB_PASSWORD'),
    db_host=os.getenv('DB_HOST'),
    db_port=os.getenv('DB_PORT'),
)

TG_CONFIG = TGConfig(
    api_id=int(os.getenv('API_ID')),
    api_hash=os.getenv('API_HASH'),
)
