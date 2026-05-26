from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Bunny, Photo
from app.schemas import CreatePhotoPayload, PhotoSchema, UpdatePhotoPayload
from app.services.bootstrap import photo_to_schema
from app.storage import get_storage
from app.utils import new_id, normalize_dot_date, year_from_date

router = APIRouter(prefix="/photos", tags=["photos"])


def _get_photo(db: Session, photo_id: str) -> Photo:
    photo = db.get(Photo, photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return photo


@router.post("", response_model=PhotoSchema, status_code=201)
def create_photo(payload: CreatePhotoPayload, db: Session = Depends(get_db)) -> PhotoSchema:
    bunny = db.get(Bunny, payload.bunnyId)
    if not bunny:
        raise HTTPException(status_code=404, detail="Bunny not found")
    tags = payload.tags if payload.tags else [bunny.name]
    photo = Photo(
        id=new_id("p"),
        bunny_id=payload.bunnyId,
        src_path=payload.src,
        photo_date=normalize_dot_date(payload.date),
        description=payload.description,
        year=payload.year or year_from_date(payload.date),
    )
    photo.tags = tags
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo_to_schema(photo)


@router.patch("/{photo_id}", response_model=PhotoSchema)
def update_photo(
    photo_id: str,
    payload: UpdatePhotoPayload,
    db: Session = Depends(get_db),
) -> PhotoSchema:
    photo = _get_photo(db, photo_id)
    data = payload.model_dump(exclude_unset=True)
    if "src" in data and data["src"] is not None:
        old = photo.src_path
        photo.src_path = data["src"]
        if old.startswith("/uploads/") and old != data["src"]:
            get_storage().delete_by_url(old)
    if "date" in data and data["date"] is not None:
        photo.photo_date = normalize_dot_date(data["date"])
    if "description" in data:
        photo.description = data["description"]
    if "year" in data and data["year"] is not None:
        photo.year = data["year"]
    if "tags" in data and data["tags"] is not None:
        photo.tags = data["tags"]
    db.commit()
    db.refresh(photo)
    return photo_to_schema(photo)


@router.delete("/{photo_id}", status_code=204)
def delete_photo(photo_id: str, db: Session = Depends(get_db)) -> None:
    photo = _get_photo(db, photo_id)
    storage = get_storage()
    url = photo.src_path
    db.delete(photo)
    db.commit()
    storage.delete_by_url(url)
