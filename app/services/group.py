from uuid import UUID

from fastapi import HTTPException
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
        data: GroupCreate,
        user_id: UUID
    ) -> GroupRead:
        if not data.type:
            raise HTTPException(
                status_code=400,
                detail=CHAT_FIELD_ERROR.format('group', 'type: group')
            )
        if not data.name:
            raise HTTPException(
                status_code=400,
                detail=CHAT_FIELD_ERROR.format('group', 'name')
            )
        if not data.members:
            raise HTTPException(
                status_code=400,
                detail=CHAT_FIELD_ERROR.format('group', 'members')
            )
        chat = await chat_repo.create(
            session, name=data.name, type_chat='group'
        )
        group = await group_repo.create_group(
            session, creator_id=user_id, chat_id=chat.id
        )
        await chat_repo.add_members(session, chat.id, [user_id, *data.members])
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
                status_code=404, detail=CHAT_NOT_FOUND.format(group_id)
            )
        if not await chat_repo.is_user_member(session, group.chat_id, user_id):
            raise HTTPException(
                status_code=403,
                detail=CHAT_FORBIDDEN.format(user_id, group_id)
            )
        return cls.create_group_read(group)

    @staticmethod
    async def update_group(
        session: AsyncSession,
        group_id: UUID,
        data: GroupUpdate
    ) -> GroupRead:
        grp = await group_repo.get(session, group_id)
        return await group_repo.update(session, grp, data)

    @staticmethod
    async def delete_group(
        session: AsyncSession,
        group_id: UUID,
        user_id: UUID
    ) -> None:
        group = await group_repo.get(group_id, session)
        if not group:
            raise HTTPException(
                status_code=404, detail=CHAT_NOT_FOUND.format(group_id)
            )
        if not await group_repo.is_user_creator(session, group_id, user_id):
            raise HTTPException(
                status_code=403,
                detail=CHAT_FORBIDDEN.format(user_id, group_id)
            )
        await group_repo.remove(group, session)
