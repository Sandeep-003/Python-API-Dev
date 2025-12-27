
from sqlalchemy import create_engine


from sqlalchemy.orm import sessionmaker

SQL_ALCHEMY_DB_URL = 'postgresql://postgres:lunar@localhost/pyapp'

engine = create_engine(SQL_ALCHEMY_DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
