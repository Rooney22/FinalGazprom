from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.settings import settings
from sqlalchemy.engine import URL


connection_string = URL.create(
    drivername='postgresql',
    username=settings.login,
    password=settings.password,
    host=settings.base_host,
    port=settings.base_port,
    database=settings.base_name,
)

engine = create_engine(
    connection_string
)

Session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
)


def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()
