from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_USER = "root"
DATABASE_PASSWORD = ""
DATABASE_HOST = "127.0.0.1"
DATABASE_PORT = "3306"
DATABASE_NAME = "kmcdb"

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"  # SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = "mysql://{}:{}@{}:{}/{}".format(
DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT,
DATABASE_NAME)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
print(
    "Connected to DATABASE: "
    + DATABASE_HOST
    + ":"
    + str(DATABASE_PORT)
    + "/"
    + DATABASE_NAME
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()