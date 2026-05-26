"""Create tables and populate from scripts/initial_seed.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_ROOT))

from app.database import Base, SessionLocal, engine  # noqa: E402
from app.models import (  # noqa: E402
    AppSetting,
    Bunny,
    HealthRecord,
    Photo,
    TimelineEvent,
    WeightRecord,
)
from app.services.bootstrap import CURRENT_BUNNY_KEY  # noqa: E402

SEED_PATH = Path(__file__).resolve().parent / "initial_seed.json"


def _wipe(db) -> None:
    for model in (Photo, HealthRecord, WeightRecord, TimelineEvent, Bunny, AppSetting):
        db.query(model).delete()
    db.commit()


def _load(db, data: dict) -> None:
    for bunny in data["bunnies"]:
        db.add(
            Bunny(
                id=bunny["id"],
                name=bunny["name"],
                breed=bunny["breed"],
                birth_date=bunny["birthDate"],
                avatar_path=bunny["avatar"],
                weight=bunny["weight"],
                notes=bunny.get("notes"),
            )
        )

    for bunny_id, bundle in data["bunnyData"].items():
        for event in bundle["timelineEvents"]:
            row = TimelineEvent(
                id=event["id"],
                bunny_id=bunny_id,
                event_date=event["date"],
                title=event["title"],
                cover_image_path=event["coverImage"],
                description=event["description"],
                mood=event["mood"],
                color=event["color"],
            )
            row.detail_images = event.get("detailImages", [])
            db.add(row)

        for record in bundle["weightRecords"]:
            db.add(
                WeightRecord(
                    id=record["id"],
                    bunny_id=bunny_id,
                    record_date=record["date"],
                    weight=record["weight"],
                )
            )

        for photo in bundle["photos"]:
            row = Photo(
                id=photo["id"],
                bunny_id=bunny_id,
                src_path=photo["src"],
                photo_date=photo["date"],
                description=photo.get("description", ""),
                year=photo["year"],
            )
            row.tags = photo.get("tags", [])
            db.add(row)

        for record in bundle["healthRecords"]:
            db.add(
                HealthRecord(
                    id=record["id"],
                    bunny_id=bunny_id,
                    record_date=record["date"],
                    type=record["type"],
                    description=record["description"],
                    status=record["status"],
                )
            )

    db.add(AppSetting(key=CURRENT_BUNNY_KEY, value=data["currentBunnyId"]))
    db.commit()


def main() -> None:
    if not SEED_PATH.is_file():
        raise SystemExit(f"Missing seed file: {SEED_PATH}")

    Base.metadata.create_all(bind=engine)
    with SEED_PATH.open(encoding="utf-8") as f:
        data = json.load(f)

    db = SessionLocal()
    try:
        _wipe(db)
        _load(db, data)
        print(f"Seeded {len(data['bunnies'])} bunnies from {SEED_PATH.name}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
