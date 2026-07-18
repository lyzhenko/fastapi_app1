from fastapi import APIRouter

from app.services.bookings import BookingService
from app.schemas.hotels import ShemaBooking

router = APIRouter(
    prefix="/bookings",
    tags=["bookings"],
)


@router.get("/")
async def get_bookings() -> list[ShemaBooking]:
    return await BookingService.find_all()


@router.get("/{booking_id}")
async def get_booking_id(booking_id: int):
    return await BookingService.find_by_id(booking_id)
