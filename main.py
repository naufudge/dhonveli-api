from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from schemas import *
from typing import Annotated, List
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models
import pymysql
from copy import copy

app = FastAPI(title="Dhonveli API")

origins = ["http://localhost:3000", "http://localhost:3001"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

pymysql.install_as_MySQLdb()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()

@app.get("/users/{username}", status_code=status.HTTP_200_OK)
async def read_user(username: str, db: db_dependency):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/hotels/", status_code=status.HTTP_201_CREATED)
async def add_hotel(hotel: CreateHotel, db: db_dependency):  
    db_hotel = models.Hotel(name=hotel.name, room_count=0)
    
    db.add(db_hotel)
    db.commit()

    # room_types = [
    #     models.RoomType(
    #         name=room["name"],
    #         price=room["price"],
    #         bed_count=room["bed_count"],
    #         quantity=room["quantity"],
    #         hotel_id=db_hotel.id
    #     ) for room in hotel.rooms
    # ]

    # db.add_all(room_types)
    # db.commit()


@app.get("/hotels/", response_model=List[ViewHotel],  status_code=status.HTTP_200_OK)
async def get_hotels(db: db_dependency):
    hotels = db.query(models.Hotel).all()
    if not hotels:
        raise HTTPException(status_code=404, detail="No hotels found")
    return hotels

@app.patch("/hotels/{hotel_id}", status_code=status.HTTP_200_OK)
async def update_hotel(hotel_id: int, hotel_update: CreateHotel, db: db_dependency):
    """Create new room types for an individual hotel."""
    hotel = db.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()

    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    
    if hotel_update.rooms is not None:
        room_count = copy(hotel.room_count)
        for room in hotel_update.rooms:
            room_count += room["quantity"]
        
        hotel.room_count = room_count

    room_types = [
        models.RoomType(
            name=room["name"],
            price=room["price"],
            bed_count=room["bed_count"],
            quantity=room["quantity"],
            hotel_id=hotel.id
        ) for room in hotel_update.rooms
    ]

    db.add_all(room_types)
    db.commit()
    db.refresh(hotel)



@app.get("/room_types/", response_model=List[HotelRoomTypes], status_code=status.HTTP_200_OK)
async def get_room_types(db: db_dependency):
    room_types = db.query(models.RoomType).all()
    if not room_types:
        raise HTTPException(status_code=404, detail="No hotel room types found")
    return room_types