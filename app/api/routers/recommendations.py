from fastapi import APIRouter

router = APIRouter()


@router.get('/recommendations')
async def get_recommendations(
        recommendations_service,
        uid: str,
):
    await recommendations_service.get_recommendations(uid=uid)

