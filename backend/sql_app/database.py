import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def get_db_path():
    db_dir = os.path.join(os.path.expanduser('~'), 'pantalone', 'db')
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    return os.path.join(db_dir, 'pantalone.db')

SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///{get_db_path()}"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
)

SessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()