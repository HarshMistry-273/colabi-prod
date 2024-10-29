import pymongo
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from src.config import Config
from sqlalchemy.orm import scoped_session
from contextlib import contextmanager
from typing import Generator

engine = create_engine(Config.DATABSE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

# Create a scoped session
ScopedSession = scoped_session(SessionLocal)


def get_db_session():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


@contextmanager
def get_db_session_celery() -> Generator:
    """
    Context manager for handling database sessions safely
    """
    session = ScopedSession()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()
        ScopedSession.remove()


db = SessionLocal()

try:
    # Creating a MongoClient to connect to the local MongoDB server
    client = pymongo.MongoClient(Config.MONGODB_URL)

    # Selecting a specific database named 'your_database_name'
    database = client[Config.MONGODB_DB_NAME]
except Exception as e:
    print(f"Error: {e}")


def get_collection():
    collection = database[Config.MONGODB_COLLECTION_NAME]
    yield collection


# cnx = mysql.connector.connect(
#     host=Config.MYSQL_HOST_NAME,
#     port=Config.MYSQL_PORT,
#     user=Config.MYSQL_USERNAME,
#     password=Config.MYSQL_PASSWORD,
#     database=Config.MYSQL_DATABASE
# )

# def get_db_cursor():
#     cur = cnx.cursor()
#     try:
#         yield cur
#     except Exception as e:
#         raise e
#     finally:
#         cur.close()