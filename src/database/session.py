from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import DB_CONFIG


engine = create_async_engine(
    DB_CONFIG.get_connection_url(),
    echo=True,
)

session_factory = async_sessionmaker(
    bind=engine,
    autocommit=False,
    expire_on_commit=False,
)
