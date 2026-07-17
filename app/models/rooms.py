from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from app.database import Base


class Rooms(Base):
    __tablename__ = "rooms"

    id: Column = Column(Integer, primary_key=True, nullable=False)
    hotel_id: Column = Column(ForeignKey("hotels.id"), nullable=False)
    name: Column = Column(String, nullable=False)
    description: Column = Column(String, nullable=False)
    price: Column = Column(Integer, nullable=False)
    service: Column = Column(JSON, nullable=False)
    quantity: Column = Column(Integer, nullable=False)
    image_id: Column = Column(Integer)
