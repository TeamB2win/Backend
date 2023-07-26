def get_data():
  ...
  
def query_data():
  ...

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "경로"

engine = create_engine(DATABASE_URL, echo=True)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()