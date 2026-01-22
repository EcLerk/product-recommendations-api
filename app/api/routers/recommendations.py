from typing import Any

from fastapi import APIRouter, Depends

from app.services.recommendations import RecommendationsService

router = APIRouter()


@router.get('/')
def get_recommendations(
        user_id: int,
        recommendations_service: RecommendationsService = Depends(),
) -> dict[str, Any]:
    return recommendations_service.get_user_recommendations(user_id=user_id)

