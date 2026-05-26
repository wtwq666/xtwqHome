from fastapi import APIRouter

from app.routers import bunnies, health, photos, settings, timeline, uploads, weights

api_router = APIRouter(prefix="/api")

api_router.include_router(settings.router)
api_router.include_router(bunnies.router)
api_router.include_router(timeline.router)
api_router.include_router(weights.router)
api_router.include_router(health.router)
api_router.include_router(photos.router)
api_router.include_router(uploads.router)
