from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Get database session
    :return: database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
