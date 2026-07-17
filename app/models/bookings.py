from sqlalchemy import Column, Integer, Date, ForeignKey, Computed
from app.database import Base


class Bookings(Base):
    """
    Модель для представления бронирований номеров в отеле.

    Хранит информацию о бронировании: номер, пользователь, даты, цену и расчётные поля.

    Attributes:
        id: Уникальный идентификатор бронирования (первичный ключ).
        room_id: ID номера, который забронирован (внешний ключ на rooms).
        user_id: ID пользователя, который забронировал номер (внешний ключ на users).
        date_from: Дата начала бронирования.
        date_to: Дата окончания бронирования.
        price: Цена номера за одни сутки.
        total_cost: Вычисляемое поле - общая стоимость бронирования (дни * цена).
        total_days: Вычисляемое поле - количество дней бронирования.
    """

    __tablename__ = "bookings"

    id: Column = Column(Integer, primary_key=True)
    room_id: Column = Column(ForeignKey("rooms.id"))
    user_id: Column = Column(ForeignKey("users.id"))
    date_from: Column = Column(Date, nullable=False)
    date_to: Column = Column(Date, nullable=False)
    price: Column = Column(Integer, nullable=False)
    total_cost: Column = Column(Integer, Computed("(date_from - date_to) * price"))
    total_days: Column = Column(Integer, Computed("date_from - date_to"))
