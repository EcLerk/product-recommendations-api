from fastapi import APIRouter

from app.api.routers.recommendations import router as recommendations_router

api_router = APIRouter()

api_router.include_router(recommendations_router, prefix="/recommendations")