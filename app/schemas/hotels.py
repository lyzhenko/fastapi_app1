from datetime import date

from pydantic import BaseModel


class ShemaBooking(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int

    class Config:
        orm_mode = True


class ShemaHotel(BaseModel):
    address: str
    name: str
    starts: int
