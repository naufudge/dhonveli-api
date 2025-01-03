from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any
from datetime import datetime


class UserBase(BaseModel):
    username: str
    password: str
    email: str
    loyalty_points: int
    role: str

class User(BaseModel):
    id: int
    username: str
    email: str
    loyalty_points: int
    role: str

class UserUpdate(BaseModel):
    loyalty_points: int | None = None
    role: str | None = None

class CreateHotel(BaseModel):
    name: str | None = None
    rooms: List[Dict[str, str | int | float]] | None = None

class ViewHotel(BaseModel):
    id: int
    name: str
    room_count: int
    

class CreateHotelRoomType(BaseModel):
    hotel_id: int | None = None
    rooms: List[Dict[str, str | int | float]] | None = None

class UpdateHotelRoomType(BaseModel):
    name: str
    price: float
    bed_count: int

class HotelRoomType(BaseModel):
    id: int
    name: str
    price: float
    bed_count: int
    quantity: int
    hotel_id: int
    hotel: ViewHotel

class HotelRoom(BaseModel):
    id: int | None = None
    room_number: int | None = None
    occupied: bool | None = None
    bookings: List | None = None
    room_type_id: int
    room_type: HotelRoomType | None = None


class CreateHotelRoom(BaseModel):
    hotel_room: HotelRoom
    hotel_id: int | None = None

class UpdateHotelRoom(BaseModel):
    room_number: int | None = None
    occupied: bool | None = None
    room_type_id: int | None = None

class HotelBookingBase(BaseModel):
    id: int
    # check_in_date: datetime
    # check_out_date: datetime
    # booking_date: datetime
    total_price: float
    numOfGuests: int
    user_id: int
    user: User
    rooms: List[HotelRoom]


class CreateHotelBooking(BaseModel):
    check_in_date: datetime | Any | None = None
    check_out_date: datetime | Any | None = None
    booking_date: datetime | Any | None = None
    numOfGuests: int | None = None
    total_price: float | None = None
    user_id: int | None = None
    room_ids: List[int] | None = None

class Activity(BaseModel):
    id: int | None = None
    name: str | None = None
    description: str | None = None
    price: int | None = None

class ActivityTicket(BaseModel): 
    id: int | None = None
    date_time: datetime | None = None
    total_price: int | None = None
    activity_id: int | None = None
    activity: Activity | None = None
    user_id: int | None = None
    user: User | None = None
