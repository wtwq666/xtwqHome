from typing import Protocol

from fastapi import UploadFile

from app.config import settings
from app.storage.local import LocalStorage
from app.storage.oss import OssStorage


class StorageBackend(Protocol):
    async def save_upload(self, file: UploadFile) -> str: ...
    def delete_by_url(self, url: str) -> None: ...


_storage: StorageBackend | None = None


def get_storage() -> StorageBackend:
    global _storage
    if _storage is None:
        if settings.storage_backend.lower() == "oss":
            _storage = OssStorage()
        else:
            _storage = LocalStorage()
    return _storage


def reset_storage() -> None:
    global _storage
    _storage = None
