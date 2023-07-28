def get_data():
  ...
  
def query_data():
  ...

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

HOSTNAME = '127.0.0.1'
PORT = 3306
USERNAME = 'example'
PASSWORD = '1234'
DBNAME = 'criminal_data'
DATABASE_URL = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DBNAME}'

engine = create_engine(DATABASE_URL, echo=True)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()