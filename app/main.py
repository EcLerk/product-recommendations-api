from fastapi import FastAPI

from app.api import init_rest_api

app = FastAPI()

init_rest_api(app)

