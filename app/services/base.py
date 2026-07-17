from sqlalchemy.orm import DeclarativeBase
from typing import ClassVar, Type, Optional
from sqlalchemy import select

from app.database import async_session_maker


class BaseService:
    """
    Базовый класс сервиса для выполнения CRUD операций с базой данных.
    
    Предоставляет асинхронные методы для поиска записей в базе данных.
    Наследники должны установить переменную класса `model` на нужную модель SQLAlchemy.
    
    Attributes:
        model: Модель SQLAlchemy, с которой работает сервис. Должна быть переопределена в подклассе.
    
    Example:
        class HotelsService(BaseService):
            model = Hotel
        
        hotels = await HotelsService.find_all(city="Moscow")
        hotel = await HotelsService.find_by_id(1)
    """

    model: ClassVar[Optional[Type[DeclarativeBase]]] = None

    @classmethod
    async def find_all(cls, **kwargs):
        """
        Получить все записи модели с опциональной фильтрацией.
        
        Args:
            **kwargs: Параметры фильтрации (например, city="Moscow", status="active").
        
        Returns:
            list: Список всех найденных записей, соответствующих фильтрам.
        
        Raises:
            NotImplementedError: Если модель не установлена в подклассе.
        """
        if cls.model is None:
            raise NotImplementedError("Model class must be set in subclass")

        async with async_session_maker() as session:
            quuery = select(cls.model).filter_by(**kwargs)
            result = await session.execute(quuery)
            return result.scalars().all()

    @classmethod
    async def find_one_or_none(cls, **kwargs):
        """
        Получить одну запись или None, если не найдена.
        
        Args:
            **kwargs: Параметры фильтрации.
        
        Returns:
            Найденная запись или None.
        
        Raises:
            NotImplementedError: Если модель не установлена в подклассе.
        """
        if cls.model is None:
            raise NotImplementedError("Model class must be set in subclass")

        async with async_session_maker() as session:
            quuery = select(cls.model).filter_by(**kwargs)
            result = await session.execute(quuery)
            return result.scalar_one_or_none()

    @classmethod
    async def find_by_id(cls, model_id: int):
        """
        Получить запись по ID.
        
        Args:
            model_id: ID записи для поиска.
        
        Returns:
            Найденная запись или None, если запись не существует.
        
        Raises:
            NotImplementedError: Если модель не установлена в подклассе.
        """
        if cls.model is None:
            raise NotImplementedError("Model class must be set in subclass")

        async with async_session_maker() as session:
            quuery = select(cls.model).filter_by(id=model_id)
            result = await session.execute(quuery)
            return result.scalar_one_or_none()
