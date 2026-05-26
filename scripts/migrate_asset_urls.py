"""将 RDS 中 /assets/ 路径替换为 OSS 公网 URL。"""

from __future__ import annotations

import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_ROOT))

from app.database import SessionLocal  # noqa: E402
from app.models import Bunny, Photo, TimelineEvent  # noqa: E402


def apply_url_map(url_map: dict[str, str]) -> int:
    """返回更新的字段数量。"""
    db = SessionLocal()
    updated = 0
    try:
        for bunny in db.query(Bunny).all():
            if bunny.avatar_path in url_map:
                bunny.avatar_path = url_map[bunny.avatar_path]
                updated += 1

        for event in db.query(TimelineEvent).all():
            if event.cover_image_path in url_map:
                event.cover_image_path = url_map[event.cover_image_path]
                updated += 1
            imgs = event.detail_images
            new_imgs = [url_map.get(p, p) for p in imgs]
            if new_imgs != imgs:
                event.detail_images = new_imgs
                updated += 1

        for photo in db.query(Photo).all():
            if photo.src_path in url_map:
                photo.src_path = url_map[photo.src_path]
                updated += 1

        db.commit()
    finally:
        db.close()
    return updated


if __name__ == "__main__":
    from scripts.oss_assets import upload_all_seed_assets  # noqa: E402

    mapping = upload_all_seed_assets()
    n = apply_url_map(mapping)
    print(f"Updated {n} DB fields with OSS URLs")
