from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import Group, Chat
from repositories.base import BaseRepository
from schemas.group import GroupUpdate, GroupCreate


class GroupRepository(BaseRepository[
    Group,
    GroupCreate,
    GroupUpdate
]):
    async def create_group(
        self,
        session: AsyncSession,
        creator_id: UUID,
        chat_id: UUID,
    ) -> Group:
        db_obj = Group(creator_id=creator_id, chat_id=chat_id)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_group_chat(
        self,
        session: AsyncSession,
        group_id: UUID
    ) -> Group | None:
        return (await session.execute(
            select(Group).options(
                selectinload(
                    Group.chat
                ).options(
                    selectinload(Chat.members),
                    selectinload(Chat.messages)
                )
            ).where(Group.id == group_id)
        )).scalars().first()

    async def is_user_creator(
        self,
        session: AsyncSession,
        group_id: UUID,
        user_id: UUID
    ) -> bool:
        return (await session.execute(select(
            select(Group).where(
                Group.id == group_id,
                Group.creator_id == user_id
            ).exists()
        ))).scalar()


group_repo = GroupRepository(Group)
