from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AppSetting, Bunny
from app.schemas import BunnySchema, CreateBunnyPayload
from app.services.bootstrap import (
    CURRENT_BUNNY_KEY,
    bunny_to_schema,
    get_current_bunny_id,
    set_current_bunny_id,
)
from app.services.files import collect_bunny_file_urls, delete_upload_urls
from app.storage import get_storage
from app.utils import new_id
from fastapi import UploadFile, File

router = APIRouter(prefix="/bunnies", tags=["bunnies"])


def _get_bunny(db: Session, bunny_id: str) -> Bunny:
    bunny = db.get(Bunny, bunny_id)
    if not bunny:
        raise HTTPException(status_code=404, detail="Bunny not found")
    return bunny


@router.post("", response_model=BunnySchema, status_code=201)
def create_bunny(payload: CreateBunnyPayload, db: Session = Depends(get_db)) -> BunnySchema:
    bunny_id = new_id("b")
    bunny = Bunny(
        id=bunny_id,
        name=payload.name,
        breed=payload.breed,
        birth_date=payload.birthDate,
        avatar_path=payload.avatar or "/assets/photo-11-baby.jpg",
        weight=payload.weight,
    )
    db.add(bunny)
    db.commit()
    db.refresh(bunny)
    setting = db.get(AppSetting, CURRENT_BUNNY_KEY)
    if not setting or not setting.value:
        set_current_bunny_id(db, bunny_id)
    return bunny_to_schema(bunny)


@router.patch("/{bunny_id}", response_model=BunnySchema)
def update_bunny(
    bunny_id: str,
    payload: dict,
    db: Session = Depends(get_db),
) -> BunnySchema:
    bunny = _get_bunny(db, bunny_id)
    if "name" in payload:
        bunny.name = payload["name"]
    if "breed" in payload:
        bunny.breed = payload["breed"]
    if "birthDate" in payload:
        bunny.birth_date = payload["birthDate"]
    if "avatar" in payload:
        bunny.avatar_path = payload["avatar"]
    if "weight" in payload:
        bunny.weight = int(payload["weight"])
    if "notes" in payload:
        bunny.notes = payload["notes"]
    db.commit()
    db.refresh(bunny)
    return bunny_to_schema(bunny)


@router.delete("/{bunny_id}", status_code=204)
def delete_bunny(bunny_id: str, db: Session = Depends(get_db)) -> None:
    bunny = _get_bunny(db, bunny_id)
    urls = collect_bunny_file_urls(db, bunny_id)
    was_current = get_current_bunny_id(db) == bunny_id
    db.delete(bunny)
    db.commit()
    delete_upload_urls(urls)
    if was_current:
        next_bunny = db.query(Bunny).order_by(Bunny.id).first()
        if next_bunny:
            set_current_bunny_id(db, next_bunny.id)
        else:
            row = db.get(AppSetting, CURRENT_BUNNY_KEY)
            if row:
                db.delete(row)
                db.commit()


@router.post("/{bunny_id}/avatar", response_model=dict)
async def upload_avatar(
    bunny_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> dict[str, str]:
    bunny = _get_bunny(db, bunny_id)
    storage = get_storage()
    old = bunny.avatar_path
    url = await storage.save_upload(file)
    bunny.avatar_path = url
    db.commit()
    if old and not old.startswith("/assets/"):
        storage.delete_by_url(old)
    return {"url": url}
