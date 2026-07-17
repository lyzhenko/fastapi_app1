from sqlalchemy.orm import DeclarativeBase
from typing import ClassVar, Type, Optional
from sqlalchemy import select

from app.database import async_session_maker


class BaseService:
    model: ClassVar[Optional[Type[DeclarativeBase]]] = None

    @classmethod
    async def find_all(cls):
        if cls.model is None:
            raise NotImplementedError("Model class must be set in subclass")

        async with async_session_maker() as session:
            quuery = select(cls.model)
            result = await session.execute(quuery)
            return result.scalars().all()
