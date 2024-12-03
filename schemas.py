from pydantic import BaseModel
from typing import List, Dict, Any


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
    booking_id: int | None = None
    booking: Any | None = None
    room_type_id: int
    room_type: HotelRoomType | None = None

class CreateHotelRoom(BaseModel):
    hotel_room: HotelRoom
    hotel_id: int | None = None

class UpdateHotelRoom(BaseModel):
    room_number: int | None = None
    occupied: bool | None = None
    room_type_id: int | None = None