from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from dependencies.database import get_async_session
from dependencies.auth import current_user
from models import User
from schemas.chat import ChatCreate, ChatRead
from services.chat import ChatService

router = APIRouter()

@router.post('/', response_model=ChatRead)
async def create_chat(
    data: ChatCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    try:
        chat = await ChatService.create_chat(session, data, user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return chat

@router.get('/{chat_id}', response_model=ChatRead)
async def read_chat(
    chat_id: UUID,
    session: AsyncSession = Depends(get_async_session),
    user = Depends(current_user),
):
    return await ChatService.get_chat_for_user(session, chat_id, user.id)

@router.get('/', response_model=list[ChatRead])
async def list_chats_for_user(
    limit: int = 10,
    offset: int = 0,
    session: AsyncSession = Depends(get_async_session),
    user = Depends(current_user),
):
    return await ChatService.list_chats_for_user(
        session, user.id, limit, offset
    )
