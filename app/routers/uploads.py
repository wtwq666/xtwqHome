from fastapi import APIRouter, Depends, File, UploadFile

from app.schemas import UploadResponse
from app.storage import get_storage

router = APIRouter(prefix="/uploads", tags=["uploads"])


@router.post("", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)) -> UploadResponse:
    storage = get_storage()
    url = await storage.save_upload(file)
    return UploadResponse(url=url)
