from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models import Chat
from repositories.chat import chat_repo
from schemas.chat import ChatCreate

class ChatService:
    @staticmethod
    async def create_chat(
        session: AsyncSession,
        data: ChatCreate,
        user_id: UUID
    ) -> Chat:
        if data.type == 'private':
            if not data.other_user_id:
                raise HTTPException(
                    status_code=400,
                    detail='Для private-чата необходимо указать other_user_id'
                )
            if await chat_repo.private_chat_exists(
                session, user_id, data.other_user_id
            ):
                raise HTTPException(
                    status_code=400,
                    detail='Приватный чат между этими пользователями уже существует'
                )
        chat = await chat_repo.create(data, session)
        await chat_repo.add_member(session, chat.id, user_id)
        if data.type == 'private':
            await chat_repo.add_member(session, chat.id, data.other_user_id)
        return chat

    @staticmethod
    async def get_chat_for_user(
        session: AsyncSession,
        chat_id: UUID,
        user_id: UUID
    ) -> Chat:
        chat = await chat_repo.get(session, chat_id)
        if not chat:
            raise HTTPException(status_code=404, detail='Чат не найден')
        is_member = await chat_repo.is_user_member(session, chat_id, user_id)
        if not is_member:
            raise HTTPException(status_code=403, detail='Доступ запрещён')
        return chat

    @staticmethod
    async def list_chats_for_user(
        session: AsyncSession,
        user_id: UUID,
        limit: int,
        offset: int
    ) -> list[Chat]:
        return await chat_repo.get_for_user(
            session,
            user_id,
            limit=limit,
            offset=offset
        )
