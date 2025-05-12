from fastapi import APIRouter

from api.chat import router as chat_router
from api.user import router as user_router


router = APIRouter()
router.include_router(chat_router, prefix='/chat', tags=['chat'])
router.include_router(user_router)
