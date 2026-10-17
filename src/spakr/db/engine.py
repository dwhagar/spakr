"""SQLAlchemy engine creation (MySQL 8 through PyMySQL)."""

from sqlalchemy import Engine, create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session, sessionmaker

from spakr.config import Settings

# Below MySQL's default wait_timeout (8 hours) with a wide margin.
POOL_RECYCLE_SECONDS = 1800
POOL_SIZE = 8


def database_url(settings: Settings) -> URL:
    """Build the connection URL from the manual-only database section."""
    db = settings.database
    query = {"charset": "utf8mb4"}
    if db.socket:
        query["unix_socket"] = db.socket
        return URL.create("mysql+pymysql", username=db.user, password=db.password.reveal(),
                          database=db.name, query=query)
    return URL.create("mysql+pymysql", username=db.user, password=db.password.reveal(),
                      host=db.host, port=db.port, database=db.name, query=query)


def create_db_engine(settings: Settings) -> Engine:
    """Create the engine. Does not connect until first use."""
    return create_engine(
        database_url(settings),
        pool_pre_ping=True,
        pool_recycle=POOL_RECYCLE_SECONDS,
        pool_size=POOL_SIZE,
    )


def session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(engine, expire_on_commit=False)
