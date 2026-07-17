from app.models.bookings import Bookings
from app.services.base import BaseService


class BookingService(BaseService):
    """
    Сервис для управления бронированиями.

    Наследует методы поиска от BaseService и работает с моделью Bookings.
    Предоставляет асинхронные методы для получения данных о бронированиях.

    Example:
        booking = await BookingService.find_by_id(1)
        all_bookings = await BookingService.find_all()
        user_bookings = await BookingService.find_all(user_id=1)
    """

    model = Bookings
