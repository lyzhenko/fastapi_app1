from sqlalchemy import Column, Integer, String
from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id: Column = Column(Integer, primary_key=True, nullable=False)
    email: Column = Column(String, nullable=False)
    hashed_password: Column = Column(String, nullable=False)
