from sqlalchemy import Column, Integer, String, JSON
from app.database import Base


class Hotels(Base):
    """
    Модель для представления отелей в системе.

    Хранит информацию об отелях, включая название, местоположение,
    доступные услуги и количество номеров.

    Attributes:
        id: Уникальный идентификатор отеля (первичный ключ).
        name: Название отеля.
        location: Местоположение/адрес отеля.
        services: JSON поле со списком услуг, предоставляемых отелем.
        rooms_quanyity: Количество номеров в отеле.
        image_id: ID изображения отеля.
    """

    __tablename__ = "hotels"
    id: Column = Column(Integer, primary_key=True)
    name: Column = Column(String, nullable=False)
    location: Column = Column(String, nullable=False)
    services: Column = Column(JSON)
    rooms_quanyity: Column = Column(Integer, nullable=False)
    image_id: Column = Column(Integer)
