from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from libs.utils.path import get_db_path


SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///{get_db_path()}"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
)

SessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()