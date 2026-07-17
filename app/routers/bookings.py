from fastapi import APIRouter

from app.services.bookings import BookingService

router = APIRouter(
    prefix="/bookings",
    tags=["bookings"],
)


@router.get("/")
async def get_bookings():
    return await BookingService.find_all()


@router.get("/{booking_id}")
async def get_booking_id(booking_id: int):
    return await BookingService.find_by_id(booking_id)
