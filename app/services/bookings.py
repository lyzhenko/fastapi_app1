from app.models.bookings import Bookings
from app.services.base import BaseService


class BookingService(BaseService):
    model = Bookings
