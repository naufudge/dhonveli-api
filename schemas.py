from pydantic import BaseModel
from typing import List, Dict


class UserBase(BaseModel):
    username: str
    password: str
    email: str
    loyalty_points: int
    role: str


class CreateHotel(BaseModel):
    name: str
    rooms: List[Dict[str, str | int | float]]

class ViewHotel(BaseModel):
    name: str
    room_count: int
    