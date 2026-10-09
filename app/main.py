from fastapi import FastAPI
from app.api.v1.api_router import router

app = FastAPI(title="Project", version="1.0")

app.include_router(router, prefix="")