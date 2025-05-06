from models import Group
from repositories.base import BaseRepository
from schemas.group import GroupUpdate, GroupCreate


class GroupRepository(BaseRepository[
    Group,
    GroupCreate,
    GroupUpdate
]):
    pass


group_repo = GroupRepository(Group)
