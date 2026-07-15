from pydantic import BaseModel
from datetime import date

class ShemaBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date

class ShemaHotel(BaseModel):    
    address: str
    name: str
    starts: int