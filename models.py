from sqlalchemy import Boolean, Column, Integer, String
from database import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    password = Column()
    loyalty_points = Column(Integer)
    role = Column(String(50))

class Hotels(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
