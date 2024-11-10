from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm.decl_api import DeclarativeBase
from dotenv import load_dotenv
import os
from typing import Any

load_dotenv()

URL = os.getenv("DB_URL")

engine = create_engine(URL)

SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind=engine)

Base: DeclarativeBase | Any = declarative_base()
