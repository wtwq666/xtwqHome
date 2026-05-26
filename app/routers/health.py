from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Bunny, HealthRecord
from app.schemas import CreateHealthRecordPayload, HealthRecordSchema, UpdateHealthRecordPayload
from app.services.bootstrap import health_to_schema
from app.utils import new_id, normalize_dot_date

router = APIRouter(prefix="/health-records", tags=["health"])


def _get_record(db: Session, record_id: str) -> HealthRecord:
    record = db.get(HealthRecord, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Health record not found")
    return record


@router.post("", response_model=HealthRecordSchema, status_code=201)
def create_health_record(
    payload: CreateHealthRecordPayload,
    db: Session = Depends(get_db),
) -> HealthRecordSchema:
    if not db.get(Bunny, payload.bunnyId):
        raise HTTPException(status_code=404, detail="Bunny not found")
    record = HealthRecord(
        id=new_id("h"),
        bunny_id=payload.bunnyId,
        record_date=normalize_dot_date(payload.date),
        type=payload.type,
        description=payload.description,
        status=payload.status,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return health_to_schema(record)


@router.patch("/{record_id}", response_model=HealthRecordSchema)
def update_health_record(
    record_id: str,
    payload: UpdateHealthRecordPayload,
    db: Session = Depends(get_db),
) -> HealthRecordSchema:
    record = _get_record(db, record_id)
    data = payload.model_dump(exclude_unset=True)
    if "date" in data and data["date"] is not None:
        record.record_date = normalize_dot_date(data["date"])
    if "type" in data:
        record.type = data["type"]
    if "description" in data:
        record.description = data["description"]
    if "status" in data:
        record.status = data["status"]
    db.commit()
    db.refresh(record)
    return health_to_schema(record)


@router.delete("/{record_id}", status_code=204)
def delete_health_record(record_id: str, db: Session = Depends(get_db)) -> None:
    record = _get_record(db, record_id)
    db.delete(record)
    db.commit()
