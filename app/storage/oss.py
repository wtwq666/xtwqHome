from __future__ import annotations

import uuid
from functools import lru_cache
from urllib.parse import urlparse

import alibabacloud_oss_v2 as oss
from fastapi import UploadFile

from app.config import settings


@lru_cache
def _oss_client() -> oss.Client:
    cfg = oss.config.load_default()
    cfg.credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
    cfg.region = settings.oss_region
    return oss.Client(cfg)


class OssStorage:
    """阿里云 OSS：对象写入 bucket 的 oss_prefix 目录，返回公网 HTTPS URL。"""

    def __init__(self) -> None:
        self.bucket = settings.oss_bucket
        self.public_base = settings.oss_public_base.rstrip("/")
        self.client = _oss_client()

    def _public_url(self, key: str) -> str:
        return f"{self.public_base}/{key.lstrip('/')}"

    def _key_from_url(self, url: str) -> str | None:
        if url.startswith("/uploads/"):
            return None
        parsed = urlparse(url)
        host = parsed.netloc
        expected = f"{self.bucket}.{settings.oss_endpoint_host}"
        if host != expected:
            return None
        return parsed.path.lstrip("/")

    async def save_upload(self, file: UploadFile) -> str:
        ext = "jpg"
        if file.filename and "." in file.filename:
            ext = file.filename.rsplit(".", 1)[-1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        key = settings.oss_key(filename)
        content = await file.read()
        self.client.put_object(
            oss.PutObjectRequest(
                bucket=self.bucket,
                key=key,
                body=content,
            )
        )
        return self._public_url(key)

    def delete_by_url(self, url: str) -> None:
        key = self._key_from_url(url)
        if not key:
            return
        try:
            self.client.delete_object(
                oss.DeleteObjectRequest(bucket=self.bucket, key=key)
            )
        except oss.exceptions.OperationError:
            pass
