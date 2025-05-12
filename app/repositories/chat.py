from typing import Sequence
from uuid import UUID

from sqlalchemy import select, exists
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
    async def create(
        self,
        session: AsyncSession,
        type_chat: str = 'private',
        name: str = 'private'
    ) -> Chat:
        chat = Chat(name=name, type=type_chat)
        session.add(chat)
        await session.commit()
        await session.refresh(chat)
        return chat

    async def get_with_members_and_messages(
        self,
        session: AsyncSession,
        chat_id: UUID
    ) -> Chat | None:
        return (await session.execute(
            select(Chat).options(
                selectinload(Chat.members),
                selectinload(Chat.messages)
            ).where(Chat.id == chat_id)
        )).scalars().first()

    async def get_chats_for_user(
        self,
        session: AsyncSession,
        user_id: UUID,
        *,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[Chat]:
        return (await session.execute(
            select(Chat).join(Chat.members).where(
                User.id == user_id
            ).options(
                selectinload(Chat.members), selectinload(Chat.messages)
            ).offset(offset).limit(limit)
        )).scalars().all()

    async def add_members(
        self,
        session: AsyncSession,
        chat_id: UUID,
        user_ids: list[UUID]
    ) -> None:
        members = [
            ChatMember(chat_id=chat_id, user_id=user_id)
            for user_id in user_ids
        ]
        session.add_all(members)
        chat = await self.get_with_members_and_messages(session, chat_id)
        try:
            await session.commit()
            await session.refresh(chat)
        except:
            await session.rollback()
            raise

    async def private_chat_exists(
        self,
        session: AsyncSession,
        user_id_1: UUID,
        user_id_2: UUID
    ) -> bool:
        return (await session.execute(
            select(exists().where(
                Chat.type == 'private',
                Chat.members.any(id=user_id_1),
                Chat.members.any(id=user_id_2)
            ))
        )).scalars().first()

    async def is_user_member(
        self,
        session: AsyncSession,
        chat_id: UUID,
        user_id: UUID
    ) -> bool:
        return (await session.execute(select(
            select(ChatMember).where(
                ChatMember.chat_id == chat_id,
                ChatMember.user_id == user_id
            ).exists()
        ))).scalar()


chat_repo = ChatRepository(Chat)
