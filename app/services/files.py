from sqlalchemy.orm import Session

from app.models import Bunny, HealthRecord, Photo, TimelineEvent
from app.storage import get_storage


def collect_bunny_file_urls(db: Session, bunny_id: str) -> list[str]:
    urls: list[str] = []
    bunny = db.get(Bunny, bunny_id)
    if bunny and bunny.avatar_path:
        urls.append(bunny.avatar_path)
    for e in db.query(TimelineEvent).filter(TimelineEvent.bunny_id == bunny_id):
        urls.append(e.cover_image_path)
        urls.extend(e.detail_images)
    for p in db.query(Photo).filter(Photo.bunny_id == bunny_id):
        urls.append(p.src_path)
    return urls


def delete_upload_urls(urls: list[str]) -> None:
    storage = get_storage()
    for url in urls:
        storage.delete_by_url(url)
