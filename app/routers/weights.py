from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Bunny, WeightRecord
from app.schemas import (
    CreateWeightRecordPayload,
    UpdateWeightRecordPayload,
    WeightRecordSchema,
)
from app.services.bootstrap import weight_to_schema
from app.services.weight_sync import sync_bunny_weight
from app.utils import new_id, normalize_dot_date

router = APIRouter(prefix="/weight-records", tags=["weights"])


def _get_record(db: Session, record_id: str) -> WeightRecord:
    record = db.get(WeightRecord, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Weight record not found")
    return record


@router.post("", response_model=WeightRecordSchema, status_code=201)
def create_weight_record(
    payload: CreateWeightRecordPayload,
    db: Session = Depends(get_db),
) -> WeightRecordSchema:
    if not db.get(Bunny, payload.bunnyId):
        raise HTTPException(status_code=404, detail="Bunny not found")
    record = WeightRecord(
        id=new_id("w"),
        bunny_id=payload.bunnyId,
        record_date=normalize_dot_date(payload.date),
        weight=payload.weight,
    )
    db.add(record)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="该兔子在此日期已有体重记录",
        ) from e
    db.refresh(record)
    sync_bunny_weight(db, payload.bunnyId)
    return weight_to_schema(record)


@router.patch("/{record_id}", response_model=WeightRecordSchema)
def update_weight_record(
    record_id: str,
    payload: UpdateWeightRecordPayload,
    db: Session = Depends(get_db),
) -> WeightRecordSchema:
    record = _get_record(db, record_id)
    data = payload.model_dump(exclude_unset=True)
    if "date" in data and data["date"] is not None:
        record.record_date = normalize_dot_date(data["date"])
    if "weight" in data and data["weight"] is not None:
        record.weight = int(data["weight"])
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="该兔子在此日期已有体重记录",
        ) from e
    db.refresh(record)
    sync_bunny_weight(db, record.bunny_id)
    return weight_to_schema(record)


@router.delete("/{record_id}", status_code=204)
def delete_weight_record(record_id: str, db: Session = Depends(get_db)) -> None:
    record = _get_record(db, record_id)
    bunny_id = record.bunny_id
    db.delete(record)
    db.commit()
    sync_bunny_weight(db, bunny_id)
