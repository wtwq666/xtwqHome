import uuid
from pathlib import Path

from fastapi import UploadFile

from app.config import get_upload_dir


class LocalStorage:
    def __init__(self, upload_dir: Path | None = None) -> None:
        self.upload_dir = upload_dir or get_upload_dir()
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def save_upload(self, file: UploadFile) -> str:
        ext = "jpg"
        if file.filename and "." in file.filename:
            ext = file.filename.rsplit(".", 1)[-1].lower()
        name = f"{uuid.uuid4().hex}.{ext}"
        dest = self.upload_dir / name
        content = await file.read()
        dest.write_bytes(content)
        return f"/uploads/{name}"

    def delete_by_url(self, url: str) -> None:
        if not url.startswith("/uploads/"):
            return
        path = self.upload_dir / url.removeprefix("/uploads/")
        if path.is_file():
            path.unlink(missing_ok=True)
