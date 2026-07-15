import uvicorn
from datetime import date
from fastapi import FastAPI, Query
from typing import Optional
from pydantic import BaseModel


app = FastAPI()


class ShemaBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date

class ShemaHotel(BaseModel):    
    address: str
    name: str
    starts: int


@app.get("/hotels", response_model=list[ShemaHotel])
def get_hotels(location: str, date_from: date, date_to: date, stars: Optional[int] = Query(None, ge=1, le=5), has_spa: Optional[bool] = False):

    hotels = [
        {
        'address': 'г. Иркутск бульвар Рябикова, 21а',
        'name': 'Super Атель',
         'starts': 5
        }

    ]
    return hotels

@app.get("/hotels/{hotel_id}", response_model=dict)
def get_hotel_by_id(hotel_id: int, date_from, date_to):    
    return {"hotel_id": hotel_id, "name": "Hotel Example", "location": "City Center", "available_from": date_from, "available_to": date_to}


@app.post('bookings', response_model=ShemaBooking)
def add_booking(booking: ShemaBooking):
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
