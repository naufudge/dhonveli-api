from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from schemas import *
from typing import Annotated, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import engine, SessionLocal
from datetime import datetime
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

@app.get("/users/", response_model=List[User], status_code=status.HTTP_200_OK)
async def get_users(db: db_dependency):
    """Get all the registered users."""
    user = db.query(models.User).all()
    if not user:
        raise HTTPException(status_code=404, detail="No users found")
    return user

@app.get("/users/{username}", status_code=status.HTTP_200_OK)
async def read_user(username: str, db: db_dependency):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.patch("/users/{username}", status_code=status.HTTP_200_OK)
async def update_user(username: str, user: UserUpdate, db: db_dependency):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.role:
        db_user.role = user.role
    if user.loyalty_points:
        db_user.loyalty_points = user.loyalty_points

    db.commit()
    db.refresh(db_user)


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

@app.post("/room_types/", status_code=status.HTTP_201_CREATED)
async def update_hotel(room_type: CreateHotelRoomType, db: db_dependency):
    """Create new room types for a hotel."""
    # hotel = db.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()

    # if not hotel:
    #     raise HTTPException(status_code=404, detail="Hotel not found")
    
    # if hotel_update.rooms is not None:
    #     room_count = copy(hotel.room_count)
    #     for room in hotel_update.rooms:
    #         room_count += room["quantity"]
        
    #     hotel.room_count = room_count

    room_types = [
        models.RoomType(
            name=room["name"],
            price=room["price"],
            bed_count=room["bed_count"],
            quantity=room["quantity"],
            hotel_id=room_type.hotel_id
        ) for room in room_type.rooms
    ]

    db.add_all(room_types)
    db.commit()

@app.patch("/room_types/{room_type_id}")
async def update_room_type(room_type_id: int, room_type_update: UpdateHotelRoomType, db: db_dependency):
    """Update the room type name, price and bed count."""
    room_type = db.query(models.RoomType).filter(models.RoomType.id == room_type_id).first()

    if not room_type:
        raise HTTPException(status_code=404, detail="Room type not found")
    
    if room_type_update.name is not None:
        room_type.name = room_type_update.name
    if room_type_update.bed_count is not None:
        room_type.bed_count = room_type_update.bed_count
    if room_type_update.price is not None:
        room_type.price = room_type_update.price
    
    db.commit()
    db.refresh(room_type)

@app.delete("/room_types/{room_type_id}")
async def delete_room_type(room_type_id: int, db: db_dependency):
    """Delete an exisitng room type."""
    deleted_count = db.query(models.RoomType).filter(models.RoomType.id == room_type_id).delete()

    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Inputted room type ID not found")
    else:
        db.commit()

@app.get("/room_types/", response_model=List[HotelRoomType], status_code=status.HTTP_200_OK)
async def get_room_types(db: db_dependency):
    room_types = db.query(models.RoomType).all()
    if not room_types:
        raise HTTPException(status_code=404, detail="No room types found")
    return room_types

@app.post("/rooms/", status_code=status.HTTP_201_CREATED)
async def create_room(room: CreateHotelRoom, db: db_dependency):
    """Create a new hotel room."""
    hotel_room = room.hotel_room
    db_room = models.Room(
        room_number = hotel_room.room_number,
        occupied = hotel_room.occupied,
        room_type_id = hotel_room.room_type_id
    )
    db_hotel = db.query(models.Hotel).filter(models.Hotel.id == room.hotel_id).first()

    if not db_hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")

    db_hotel.room_count += 1
    
    db.add(db_room)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        print(f"Integrity Error: {e}")

    db.refresh(db_hotel)

@app.get("/rooms/", response_model=List[HotelRoom], status_code=status.HTTP_200_OK)
async def get_rooms(db: db_dependency):
    """Get all hotel rooms"""
    rooms = db.query(models.Room).all()
    if not rooms:
        raise HTTPException(status_code=404, detail="No rooms found")
    
    return rooms

@app.patch("/rooms/{room_id}", status_code=status.HTTP_200_OK)
async def update_room(room_id: int, room: UpdateHotelRoom, db:db_dependency):
    """Update an existing hotel room"""
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()

    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")

    if room.room_number:
        db_room.room_number = room.room_number
    # if room.occupied:
    #     db_room.occupied = room.occupied
    if room.room_type_id:
        db_room.room_type_id = room.room_type_id
    
    db.commit()
    db.refresh(db_room)

@app.delete("/rooms/{room_id}", status_code=status.HTTP_200_OK)
async def delete_room(room_id: int, db: db_dependency):
    """Delete an existing room."""
    db_room = db.query(models.Room).filter(models.Room.id == room_id)
    room = db_room.first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    db_room_type = db.query(models.RoomType).filter(models.RoomType.id == room.room_type_id).first()
    db_hotel = db.query(models.Hotel).filter(models.Hotel.id == db_room_type.hotel_id).first()

    db_room.delete()
    
    # TODO: reduce the room count from the hotel
    db_hotel.room_count -= 1

    db.commit()
    db.refresh(db_hotel)

@app.post("/bookings/", status_code=status.HTTP_201_CREATED)
async def create_booking(booking: CreateHotelBooking, db: db_dependency):
    """Create a hotel booking a change the room status to occupied."""
    rooms: List[models.Room] = []
    for room_id in booking.room_ids:
        room = db.query(models.Room).filter(models.Room.id == room_id).first()
        if not room:
            raise HTTPException(status_code=404, detail=f"Room {room_id} not found")
        
        rooms.append(room)
        room.occupied = True

    db_booking = models.HotelBooking(
        check_in_date = datetime.fromisoformat(booking.check_in_date.replace("Z", "+00:00")).timestamp(),
        check_out_date = datetime.fromisoformat(booking.check_out_date.replace("Z", "+00:00")).timestamp(),
        booking_date = datetime.fromisoformat(booking.booking_date.replace("Z", "+00:00")).timestamp(),
        total_price = booking.total_price,
        numOfGuests = booking.numOfGuests,
        user_id = booking.user_id,
        rooms = rooms
    )

    db.add(db_booking)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        print(f"Integrity Error: {e}")
    
    for room in rooms:
        db.refresh(room)


@app.get("/bookings/", response_model=List[HotelBookingBase], status_code=status.HTTP_200_OK)
async def view_bookings(db: db_dependency):
    """Get all hotel bookings"""
    bookings = db.query(models.HotelBooking).join(models.HotelBooking.rooms).all()
    
    if not bookings:
        raise HTTPException(status_code=404, detail="No bookings found")

    return bookings
