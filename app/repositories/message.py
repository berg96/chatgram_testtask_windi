from models import Message
from repositories.base import BaseRepository
from schemas.message import MessageUpdate, MessageCreate


class MessageRepository(BaseRepository[
    Message,
    MessageCreate,
    MessageUpdate
]):
    pass


message_repo = MessageRepository(Message)
