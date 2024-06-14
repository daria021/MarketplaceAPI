from typing import TypeVar, Type

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel
from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from exceptions import NotFoundException

Schema = TypeVar("Schema", bound=BaseModel, covariant=True)
FilterSchema = TypeVar("FilterSchema", bound=Filter)
SQLModel = TypeVar("SQLModel", bound=DeclarativeBase, covariant=True)


class AbstractRepo:
    model: Type[SQLModel]
    update_schema: Type[Schema]
    create_schema: Type[Schema]
    get_schema: Type[Schema]
    filter_schema: Type[FilterSchema]

    @classmethod
    async def get(cls, session: AsyncSession, record_id: int) -> Schema | None:
        res = await session.execute(select(cls.model).where(cls.model.id == record_id))
        try:
            obj = res.scalar_one()
            return await cls.validate(obj) if obj else None
        except NoResultFound:
            raise NotFoundException

    @classmethod
    async def get_all(cls, session: AsyncSession, *filters, offset: int = 0, limit: int = 100) -> list[Schema]:
        res = await session.execute(select(cls.model).offset(offset).limit(limit).where(*filters))
        objects = res.scalars().all()
        return [await cls.validate(obj) for obj in objects]

    @classmethod
    async def get_filtered_by(cls, session: AsyncSession, filter: FilterSchema) -> list[Schema]:
        query_filter = filter.filter(select(cls.model))

        res = await session.execute(query_filter)
        objects = res.scalars().all()
        return [await cls.validate(obj) for obj in objects]

    @classmethod
    async def create(cls, session: AsyncSession, **kwargs) -> Schema:
        instance = cls.model(**kwargs)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return await cls.validate(instance)

    @classmethod
    async def update(cls, session: AsyncSession, record_id: int, **kwargs) -> Schema:
        clean_kwargs = {key: value for key, value in kwargs.items() if value is not None}
        try:
            await session.execute(update(cls.model).where(cls.model.id == record_id).values(**clean_kwargs))
            await session.commit()
            return await cls.get(session=session, record_id=record_id)
        except NoResultFound:
            raise NotFoundException

    @classmethod
    async def delete(cls, session: AsyncSession, record_id: int):
        await session.execute(delete(cls.model).where(cls.model.id == record_id))
        await session.commit()

    @classmethod
    async def validate(cls, obj: SQLModel) -> Schema:
        return cls.get_schema.model_validate(obj)
