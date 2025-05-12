from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.constants import CHAT_FIELD_ERROR, CHAT_NOT_FOUND, CHAT_FORBIDDEN
from repositories.chat import chat_repo
from repositories.group import group_repo
from schemas.group import GroupCreate, GroupUpdate, GroupRead

class GroupService:
    @staticmethod
    def create_group_read(group):
        return GroupRead(**{
            'id': group.id,
            'chat_id': group.chat.id,
            'name': group.chat.name,
            'type': group.chat.type,
            'members': group.chat.members,
            'messages': group.chat.messages,
            'creator_id': group.creator_id,
        })

    @classmethod
    async def create_group_chat(
        cls,
        session: AsyncSession,
        group_data: GroupCreate,
        user_id: UUID
    ) -> GroupRead:
        if not group_data.type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=CHAT_FIELD_ERROR.format('group', 'type: group')
            )
        if not group_data.name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=CHAT_FIELD_ERROR.format('group', 'name')
            )
        if not group_data.members:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=CHAT_FIELD_ERROR.format('group', 'members')
            )
        chat = await chat_repo.create(
            session, name=group_data.name, type_chat='group'
        )
        group = await group_repo.create_group(
            session, creator_id=user_id, chat_id=chat.id
        )
        await chat_repo.add_members(
            session, chat.id, [user_id, *group_data.members]
        )
        group = await group_repo.get_group_chat(
            session, group.id
        )
        return cls.create_group_read(group)

    @classmethod
    async def get_group_for_user(
        cls,
        session: AsyncSession,
        group_id: UUID,
        user_id: UUID
    ) -> GroupRead:
        group = await group_repo.get_group_chat(session, group_id)
        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=CHAT_NOT_FOUND.format(group_id)
            )
        if not await chat_repo.is_user_member(session, group.chat_id, user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=CHAT_FORBIDDEN.format(user_id, group_id)
            )
        return cls.create_group_read(group)

    @classmethod
    async def update_group(
        cls,
        session: AsyncSession,
        group_id: UUID,
        user_id: UUID,
        update_data: GroupUpdate
    ) -> GroupRead:
        group = await group_repo.get_group_chat(session, group_id)
        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=CHAT_NOT_FOUND.format(group_id)
            )
        if not await chat_repo.is_user_member(session, group.chat_id, user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=CHAT_FORBIDDEN.format(user_id, group_id)
            )
        if update_data.name is not None:
            group.chat.name = update_data.name
        if update_data.members is not None:
            await chat_repo.remove_all_members(session, group.chat_id)
            await chat_repo.add_members(
                session, group.chat_id, [user_id, *update_data.members]
            )
        session.add(group.chat)
        try:
            await session.commit()
        except:
            await session.rollback()
            raise
        return cls.create_group_read(group)

    @staticmethod
    async def delete_group(
        session: AsyncSession,
        group_id: UUID,
        user_id: UUID
    ) -> None:
        group = await group_repo.get(group_id, session)
        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=CHAT_NOT_FOUND.format(group_id)
            )
        if not await group_repo.is_user_creator(session, group_id, user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=CHAT_FORBIDDEN.format(user_id, group_id)
            )
        await group_repo.remove(group, session)
