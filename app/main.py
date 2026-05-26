from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import get_upload_dir, settings
from app.routers import api_router

app = FastAPI(title="臭臭的家 API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if settings.storage_backend.lower() != "oss":
    app.mount("/uploads", StaticFiles(directory=str(get_upload_dir())), name="uploads")

app.include_router(api_router)
