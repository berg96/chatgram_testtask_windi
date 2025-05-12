from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from dependencies.database import get_async_session
from dependencies.auth import current_user
from schemas.group import GroupCreate, GroupRead, GroupUpdate
from services.group import GroupService

router = APIRouter()

@router.post('/', response_model=GroupRead)
async def create_group(
    group: GroupCreate,
    session: AsyncSession = Depends(get_async_session),
    user = Depends(current_user),
):
    return await GroupService.create_group_chat(
        session, group, user.id
    )


@router.get('/{group_id}', response_model=GroupRead)
async def read_group(
    group_id: UUID,
    session: AsyncSession = Depends(get_async_session),
    user = Depends(current_user),
):
    return await GroupService.get_group_for_user(session, group_id, user.id)


@router.patch('/{group_id}', response_model=GroupRead)
async def update_group(
    group_id: UUID,
    update_data: GroupUpdate,
    session: AsyncSession = Depends(get_async_session),
    user = Depends(current_user),
):
    return await GroupService.update_group(session, group_id, user.id, update_data)


@router.delete('/{group_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(
    group_id: UUID,
    session: AsyncSession = Depends(get_async_session),
    user = Depends(current_user),
):
    return await GroupService.delete_group(session, group_id, user.id)
