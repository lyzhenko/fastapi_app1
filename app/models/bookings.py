from sqlalchemy import Column, Integer, Date, ForeignKey, Computed
from app.database import Base


class Bookings(Base):
    __tablename__ = "bookings"

    id: Column = Column(Integer, primary_key=True)
    room_id: Column = Column(ForeignKey("rooms.id"))
    user_id: Column = Column(ForeignKey("users.id"))
    date_from: Column = Column(Date, nullable=False)
    date_to: Column = Column(Date, nullable=False)
    price: Column = Column(Integer, nullable=False)
    total_cost: Column = Column(Integer, Computed("(date_from - date_to) * price"))
    total_days: Column = Column(Integer, Computed("date_from - date_to"))
