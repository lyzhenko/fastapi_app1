from sqlalchemy import JSON, Column, ForeignKey, Integer, String

from app.database import Base


class Rooms(Base):
    """
    Модель для представления номеров в отелях.

    Хранит информацию о номерах: название, описание, цену, услуги,
    количество доступных номеров данного типа и связь с отелем.

    Attributes:
        id: Уникальный идентификатор номера (первичный ключ).
        hotel_id: ID отеля, к которому относится номер (внешний ключ на hotels).
        name: Название типа номера (например, "Люкс", "Стандарт").
        description: Описание номера.
        price: Цена номера за одни сутки.
        service: JSON поле со списком услуг, включённых в номер.
        quantity: Количество доступных номеров этого типа.
        image_id: ID изображения номера.
    """

    __tablename__ = "rooms"

    id: Column = Column(Integer, primary_key=True, nullable=False)
    hotel_id: Column = Column(ForeignKey("hotels.id"), nullable=False)
    name: Column = Column(String, nullable=False)
    description: Column = Column(String, nullable=False)
    price: Column = Column(Integer, nullable=False)
    service: Column = Column(JSON, nullable=False)
    quantity: Column = Column(Integer, nullable=False)
    image_id: Column = Column(Integer)
