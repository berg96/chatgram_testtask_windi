from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.constants import (
    CHAT_FIELD_ERROR, CHAT_NOT_FOUND, CHAT_ALREADY_EXISTS, CHAT_FORBIDDEN
)
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
        if not data.type:
            raise HTTPException(
                status_code=400,
                detail=CHAT_FIELD_ERROR.format('private', 'type: private')
            )
        if not data.other_user_id:
            raise HTTPException(
                status_code=400,
                detail=CHAT_FIELD_ERROR.format('private', 'other_user_id')
            )
        if await chat_repo.private_chat_exists(
            session, user_id, data.other_user_id
        ):
            raise HTTPException(
                status_code=400,
                detail=CHAT_ALREADY_EXISTS.format(user_id, data.other_user_id)
            )
        chat = await chat_repo.create(session)
        await chat_repo.add_members(
            session, chat.id, [user_id, data.other_user_id]
        )
        return await chat_repo.get_with_members_and_messages(session, chat.id)

    @staticmethod
    async def get_chat_for_user(
        session: AsyncSession,
        chat_id: UUID,
        user_id: UUID
    ) -> Chat:
        chat = await chat_repo.get_with_members_and_messages(session, chat_id)
        if not chat:
            raise HTTPException(
                status_code=404, detail=CHAT_NOT_FOUND.format(chat_id)
            )
        if not await chat_repo.is_user_member(session, chat_id, user_id):
            raise HTTPException(
                status_code=403, detail=CHAT_FORBIDDEN.format(user_id, chat_id)
            )
        return chat

    @staticmethod
    async def list_chats_for_user(
        session: AsyncSession,
        user_id: UUID,
        limit: int,
        offset: int
    ) -> list[Chat]:
        return await chat_repo.get_chats_for_user(
            session,
            user_id,
            limit=limit,
            offset=offset
        )
