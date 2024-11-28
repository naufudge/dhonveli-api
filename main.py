from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from schemas import *
from typing import Annotated, List
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models
import pymysql

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
    room_count = 0
    for room in hotel.rooms:
        room_count += room["quantity"]
        
    db_hotel = models.Hotel(name=hotel.name, room_count=room_count)
    
    db.add(db_hotel)
    db.commit()

    room_types = [
        models.RoomType(
            name=room["name"],
            price=room["price"],
            bed_count=room["bed_count"],
            quantity=room["quantity"],
            hotel_id=db_hotel.id
        ) for room in hotel.rooms
    ]

    db.add_all(room_types)
    db.commit()


@app.get("/hotels/", response_model=List[ViewHotel],  status_code=status.HTTP_200_OK)
async def get_hotels(db: db_dependency):
    hotels = db.query(models.Hotel).all()
    if not hotels:
        raise HTTPException(status_code=404, detail="No hotels found")
    return hotels

