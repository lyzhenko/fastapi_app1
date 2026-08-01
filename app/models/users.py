from sqlalchemy import Column, Integer, String

from app.database import Base


class Users(Base):
    """
    Модель для представления пользователей системы.

    Хранит информацию об учётных записях пользователей, включая
    адрес электронной почты и хешированный пароль.

    Attributes:
        id: Уникальный идентификатор пользователя (первичный ключ).
        email: Адрес электронной почты пользователя (уникален и обязателен).
        hashed_password: Хешированный пароль пользователя (не хранится в открытом виде).
    """

    __tablename__ = "users"

    id: Column = Column(Integer, primary_key=True, nullable=False)
    email: Column = Column(String, nullable=False)
    hashed_password: Column = Column(String, nullable=False)
