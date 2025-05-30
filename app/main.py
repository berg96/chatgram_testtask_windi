from fastapi import FastAPI

from api import router as main_router
from core.config import settings


app = FastAPI(
    title=settings.app_title,
    description=settings.app_description
)
app.include_router(main_router, prefix='/api')
