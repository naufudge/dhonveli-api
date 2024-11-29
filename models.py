from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from database import Base
import pymysql

pymysql.install_as_MySQLdb()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    password = Column(String(100))
    email = Column(String(100), unique=True)
    loyalty_points = Column(Integer)
    role = Column(String(50), server_default="normal")

class Hotel(Base):
    __tablename__ = "hotel"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    room_count = Column(Integer)

class HotelBooking(Base):
    __tablename__ = "hotel_booking"

    id = Column(Integer, primary_key=True, index=True)
    check_in_date = Column(DateTime)
    check_out_date = Column(DateTime)
    booking_date = Column(DateTime)
    total_price = Column(Float)

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User")

    room_id = Column(Integer, ForeignKey("room.id", ondelete="CASCADE"), nullable=False)   
    room = relationship("Room")

    hotel_id = Column(Integer, ForeignKey("hotel.id", ondelete="CASCADE"), nullable=False)
    hotel = relationship("Hotel")


class Guest(Base):
    __tablename__ = "guest" 

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100))
    email = Column(String(100), unique=True)
    phone_number = Column(String(20))
 
 
class Room(Base):
    __tablename__ = "room"

    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String(20))

    room_type_id = Column(Integer, ForeignKey("room_type.id", ondelete="CASCADE"), nullable=False)
    room_type = relationship("RoomType")
    

class RoomType(Base):
    __tablename__ = "room_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20))
    price = Column(Float)
    bed_count = Column(Integer)
    quantity = Column(Integer)

    hotel_id = Column(Integer, ForeignKey("hotel.id", ondelete="CASCADE"), nullable=False)
    hotel = relationship("Hotel")

class Review(Base):
    __tablename__ = "review"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer)
    review = Column(String(250))
    date_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User")

    hotel_id = Column(Integer, ForeignKey("hotel.id", ondelete="CASCADE"), nullable=False)
    hotel = relationship("Hotel")

class Activity(Base):
    __tablename__ = "activity"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    description = Column(String(250))
    price = Column(Float)

class ActivityTicket(Base):
    __tablename__ = "activity_ticket"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime)
    total_price = Column(Float)
    
    activity_id = Column(Integer, ForeignKey("activity.id", ondelete="CASCADE"), nullable=False)  
    activity = relationship("Activity")

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=True)  
    user = relationship("User")
