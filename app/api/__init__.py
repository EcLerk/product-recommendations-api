from fastapi import FastAPI

from app.api.routers import api_router


def init_rest_api(app: FastAPI) -> FastAPI:
    app.include_router(api_router, prefix="/api")

    return app