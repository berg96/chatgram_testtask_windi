from typing import Generic, Type, TypeVar, Optional, List
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.db import Base

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(
        self, obj_id: UUID, session: AsyncSession
    ) -> Optional[ModelType]:
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_multi(
        self, session: AsyncSession, *, limit: int = 100, offset: int = 0,
    ) -> List[ModelType]:
        db_objs = await session.execute(
            select(self.model).offset(offset).limit(limit)
        )
        return db_objs.scalars().all()

    async def create(
        self, obj_in: CreateSchemaType, session: AsyncSession
    ) -> ModelType:
        db_obj = self.model(**obj_in.model_dump(exclude_unset=True))
        session.add(db_obj)
        try:
            await session.commit()
            await session.refresh(db_obj)
        except:
            await session.rollback()
            raise
        return db_obj

    async def update(
        self, db_obj: ModelType, obj_in: UpdateSchemaType,
        session: AsyncSession
    ) -> ModelType:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        session.add(db_obj)
        try:
            await session.commit()
            await session.refresh(db_obj)
        except:
            await session.rollback()
            raise
        return db_obj
    async def remove(
        self, db_obj: ModelType, session: AsyncSession
    ) -> ModelType | None:
        try:
            await session.delete(db_obj)
            await session.commit()
        except:
            await session.rollback()
            raise
        return db_obj