from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    password: str
    email: str
    loyalty_points: int
    role: str


class Hotel(BaseModel):
    name: str