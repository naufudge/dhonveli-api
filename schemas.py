from pydantic import BaseModel
from typing import List, Dict


class UserBase(BaseModel):
    username: str
    password: str
    email: str
    loyalty_points: int
    role: str


class CreateHotel(BaseModel):
    name: str | None = None
    rooms: List[Dict[str, str | int | float]] | None = None

class ViewHotel(BaseModel):
    id: int
    name: str
    room_count: int
    
    
class HotelRoomTypes(BaseModel):
    name: str
    price: float
    bed_count: int
    quantity: int
    hotel_id: int
    hotel: ViewHotel
