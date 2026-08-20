from sqlalchemy import create_engine
from app.database.config import *

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

from sqlalchemy import create_engine

engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"}
)