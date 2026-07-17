from sqlalchemy import Column, Integer, String, JSON
from app.database import Base


class Hotels(Base):
    __tablename__ = "hotels"
    id: Column = Column(Integer, primary_key=True)
    name: Column = Column(String, nullable=False)
    location: Column = Column(String, nullable=False)
    services: Column = Column(JSON)
    rooms_quanyity: Column = Column(Integer, nullable=False)
    image_id: Column = Column(Integer)
