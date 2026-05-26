from sqlalchemy.orm import Session

from app.models import AppSetting, Bunny, HealthRecord, Photo, TimelineEvent, WeightRecord
from app.schemas import (
    BootstrapResponse,
    BunnyDataBundleSchema,
    BunnySchema,
    HealthRecordSchema,
    PhotoSchema,
    TimelineEventSchema,
    WeightRecordSchema,
)

CURRENT_BUNNY_KEY = "current_bunny_id"


def get_current_bunny_id(db: Session, default: str = "") -> str:
    row = db.get(AppSetting, CURRENT_BUNNY_KEY)
    if row and row.value and db.get(Bunny, row.value):
        return row.value
    first = db.query(Bunny).order_by(Bunny.id).first()
    return first.id if first else default


def set_current_bunny_id(db: Session, bunny_id: str) -> None:
    bunny = db.get(Bunny, bunny_id)
    if not bunny:
        raise ValueError(f"Bunny not found: {bunny_id}")
    row = db.get(AppSetting, CURRENT_BUNNY_KEY)
    if row:
        row.value = bunny_id
    else:
        db.add(AppSetting(key=CURRENT_BUNNY_KEY, value=bunny_id))
    db.commit()


def bunny_to_schema(b: Bunny) -> BunnySchema:
    return BunnySchema(
        id=b.id,
        name=b.name,
        breed=b.breed,
        birthDate=b.birth_date,
        avatar=b.avatar_path,
        weight=b.weight,
        notes=b.notes,
    )


def timeline_to_schema(e: TimelineEvent) -> TimelineEventSchema:
    return TimelineEventSchema(
        id=e.id,
        date=e.event_date,
        title=e.title,
        coverImage=e.cover_image_path,
        description=e.description,
        detailImages=e.detail_images,
        mood=e.mood,
        color=e.color,
    )


def weight_to_schema(r: WeightRecord) -> WeightRecordSchema:
    return WeightRecordSchema(id=r.id, date=r.record_date, weight=r.weight)


def health_to_schema(r: HealthRecord) -> HealthRecordSchema:
    return HealthRecordSchema(
        id=r.id,
        date=r.record_date,
        type=r.type,  # type: ignore[arg-type]
        description=r.description,
        status=r.status,
    )


def photo_to_schema(p: Photo) -> PhotoSchema:
    return PhotoSchema(
        id=p.id,
        src=p.src_path,
        date=p.photo_date,
        description=p.description,
        year=p.year,
        tags=p.tags,
    )


def build_bootstrap(db: Session) -> BootstrapResponse:
    bunnies = db.query(Bunny).order_by(Bunny.id).all()
    current = get_current_bunny_id(db, bunnies[0].id if bunnies else "")
    bunny_data: dict[str, BunnyDataBundleSchema] = {}

    for b in bunnies:
        events = (
            db.query(TimelineEvent)
            .filter(TimelineEvent.bunny_id == b.id)
            .order_by(TimelineEvent.event_date.desc())
            .all()
        )
        weights = (
            db.query(WeightRecord)
            .filter(WeightRecord.bunny_id == b.id)
            .order_by(WeightRecord.record_date.asc())
            .all()
        )
        photos = (
            db.query(Photo)
            .filter(Photo.bunny_id == b.id)
            .order_by(Photo.photo_date.desc())
            .all()
        )
        health = (
            db.query(HealthRecord)
            .filter(HealthRecord.bunny_id == b.id)
            .order_by(HealthRecord.record_date.desc())
            .all()
        )
        bunny_data[b.id] = BunnyDataBundleSchema(
            bunny=bunny_to_schema(b),
            timelineEvents=[timeline_to_schema(e) for e in events],
            weightRecords=[weight_to_schema(r) for r in weights],
            photos=[photo_to_schema(p) for p in photos],
            healthRecords=[health_to_schema(r) for r in health],
        )

    return BootstrapResponse(
        bunnies=[bunny_to_schema(b) for b in bunnies],
        currentBunnyId=current,
        bunnyData=bunny_data,
    )
