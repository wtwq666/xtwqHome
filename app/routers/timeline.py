from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Bunny, TimelineEvent
from app.schemas import (
    CreateTimelineEventPayload,
    TimelineEventSchema,
    UpdateTimelineEventPayload,
)
from app.services.bootstrap import timeline_to_schema
from app.storage import get_storage
from app.utils import new_id, normalize_dot_date

router = APIRouter(prefix="/timeline-events", tags=["timeline"])


def _get_event(db: Session, event_id: str) -> TimelineEvent:
    event = db.get(TimelineEvent, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Timeline event not found")
    return event


@router.post("", response_model=TimelineEventSchema, status_code=201)
def create_timeline_event(
    payload: CreateTimelineEventPayload,
    db: Session = Depends(get_db),
) -> TimelineEventSchema:
    if not db.get(Bunny, payload.bunnyId):
        raise HTTPException(status_code=404, detail="Bunny not found")
    images = payload.detailImages[:9]
    cover = payload.coverImage or (images[0] if images else "")
    event = TimelineEvent(
        id=new_id("te"),
        bunny_id=payload.bunnyId,
        event_date=normalize_dot_date(payload.date),
        title=payload.title,
        cover_image_path=cover,
        description=payload.description,
        mood=payload.mood,
        color=payload.color,
    )
    event.detail_images = images
    db.add(event)
    db.commit()
    db.refresh(event)
    return timeline_to_schema(event)


@router.patch("/{event_id}", response_model=TimelineEventSchema)
def update_timeline_event(
    event_id: str,
    payload: UpdateTimelineEventPayload,
    db: Session = Depends(get_db),
) -> TimelineEventSchema:
    event = _get_event(db, event_id)
    data = payload.model_dump(exclude_unset=True)
    if "date" in data and data["date"] is not None:
        event.event_date = normalize_dot_date(data["date"])
    if "title" in data:
        event.title = data["title"]
    if "description" in data:
        event.description = data["description"]
    if "mood" in data:
        event.mood = data["mood"]
    if "color" in data:
        event.color = data["color"]
    if "detailImages" in data and data["detailImages"] is not None:
        event.detail_images = data["detailImages"]
    if "coverImage" in data and data["coverImage"] is not None:
        event.cover_image_path = data["coverImage"]
    db.commit()
    db.refresh(event)
    return timeline_to_schema(event)


@router.delete("/{event_id}", status_code=204)
def delete_timeline_event(event_id: str, db: Session = Depends(get_db)) -> None:
    event = _get_event(db, event_id)
    storage = get_storage()
    urls = [event.cover_image_path, *event.detail_images]
    db.delete(event)
    db.commit()
    for url in urls:
        storage.delete_by_url(url)
