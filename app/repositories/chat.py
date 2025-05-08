from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import Chat, User, ChatMember
from repositories.base import BaseRepository
from schemas.chat import ChatCreate, ChatUpdate


class ChatRepository(BaseRepository[
    Chat,
    ChatCreate,
    ChatUpdate
]):
    async def get_for_user(
        self,
        session: AsyncSession,
        user_id: UUID,
        *,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[Chat]:
        return await session.execute(
            select(Chat).join(Chat.members).where(
                User.id == user_id
            ).options(selectinload(Chat.members)).offset(offset).limit(limit)
        ).scalars().all()

    async def add_member(
        self,
        session: AsyncSession,
        chat_id: UUID,
        user_id: UUID
    ):
        session.add(ChatMember(chat_id=chat_id, user_id=user_id))
        try:
            await session.commit()
        except:
            await session.rollback()
            raise

    async def private_chat_exists(
        self,
        session: AsyncSession,
        user_id_1: UUID,
        user_id_2: UUID
    ) -> Chat:
        return await session.execute(
            select(Chat).join(Chat.members).where(
                Chat.type == 'private',
                Chat.members.any(id=user_id_1),
                Chat.members.any(id=user_id_2)
            )
        ).scalars.first()

    async def is_user_member(
        self,
        session: AsyncSession,
        chat_id: UUID,
        user_id: UUID
    ) -> bool:
        return await session.execute(select(
            select(ChatMember).where(
                ChatMember.chat_id == chat_id,
                ChatMember.user_id == user_id
            ).exists()
        )).scalar()



chat_repo = ChatRepository(Chat)
