from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm.decl_api import DeclarativeBase
from dotenv import load_dotenv
from typing import Any
import pymysql
import os

load_dotenv()

URL = os.getenv("DB_URL")

pymysql.install_as_MySQLdb()
engine = create_engine(URL)

SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind=engine)

Base: DeclarativeBase | Any = declarative_base()
