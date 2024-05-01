from fastapi import APIRouter

from app.endpoints import lexicomai

api_router = APIRouter()

api_router.include_router(lexicomai.router)