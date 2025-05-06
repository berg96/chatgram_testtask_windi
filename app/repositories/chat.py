from models import Chat
from repositories.base import BaseRepository
from schemas.chat import ChatCreate, ChatUpdate


class ChatRepository(BaseRepository[
    Chat,
    ChatCreate,
    ChatUpdate
]):
    pass


chat_repo = ChatRepository(Chat)
