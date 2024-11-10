from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
import pymysql

pymysql.install_as_MySQLdb()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    password = Column(String(100))
    email = Column(String(100))
    loyalty_points = Column(Integer)
    role = Column(String(50))

class Hotel(Base):
    __tablename__ = "hotel"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    number_of_rooms = Column(Integer)

class HotelBooking(Base):
    __tablename__ = "hotel_booking"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer)  
    check_in_date = Column(DateTime)
    check_out_date = Column(DateTime)
    booking_date = Column(DateTime)
    total_price = Column(Float)
    guest_id = Column(Integer)  
    room_id = Column(Integer)   

class Guest(Base):
    __tablename__ = "guest" 

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100))
    email = Column(String(100), unique=True)
    phone_number = Column(String(20))
 
 
class Room(Base):
    __tablename__ = "room"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer)  
    room_type = Column(String(50))
    room_number = Column(String(20))
    room_rate = Column(Float)
    bed_count = Column(Integer)

class Review(Base):
    __tablename__ = "review"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)  
    rating = Column(Integer)
    review = Column(String(250))
    date_time = Column(DateTime)

class Activity(Base):
    __tablename__ = "activity"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    description = Column(String(200))

class ActivityTicket(Base):
    __tablename__ = "activity_ticket"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime)
    user_id = Column(Integer, nullable=True)  
    total_price = Column(Float)
    activity_id = Column(Integer)  
