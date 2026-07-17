from sqlalchemy.orm import DeclarativeBase
from typing import ClassVar, Type, Optional
from sqlalchemy import select

from app.database import async_session_maker


class BaseService:
    model: ClassVar[Optional[Type[DeclarativeBase]]] = None

    @classmethod
    async def find_all(cls, **kwargs):
        if cls.model is None:
            raise NotImplementedError("Model class must be set in subclass")

        async with async_session_maker() as session:
            quuery = select(cls.model).filter_by(**kwargs)
            result = await session.execute(quuery)
            return result.scalars().all()

    @classmethod
    async def find_one_or_none(cls, **kwargs):
        if cls.model is None:
            raise NotImplementedError("Model class must be set in subclass")

        async with async_session_maker() as session:
            quuery = select(cls.model).filter_by(**kwargs)
            result = await session.execute(quuery)
            return result.scalar_one_or_none()

    @classmethod
    async def find_by_id(cls, model_id: int):
        if cls.model is None:
            raise NotImplementedError("Model class must be set in subclass")

        async with async_session_maker() as session:
            quuery = select(cls.model).filter_by(id=model_id)
            result = await session.execute(quuery)
            return result.scalar_one_or_none()
