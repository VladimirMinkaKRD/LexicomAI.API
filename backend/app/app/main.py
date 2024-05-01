from fastapi import FastAPI

from app.api import api_router
from app.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f'{settings.API_STR}/openapi.json',
    description='LexicomAI.API',
    version='0.1.0.alpha',
)

app.include_router(api_router, prefix=settings.API_STR)
