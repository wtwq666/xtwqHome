"""上传 app/public/assets 到 OSS，并生成 /assets/ → HTTPS URL 映射。"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import alibabacloud_oss_v2 as oss

BACKEND_ROOT = Path(__file__).resolve().parent.parent
ROOT = BACKEND_ROOT.parent
ASSETS_DIR = ROOT / "app" / "public" / "assets"
SEED_PATH = BACKEND_ROOT / "scripts" / "initial_seed.json"
SYNC_AI_SCRIPT = ROOT / "scripts" / "sync_ai_assets.py"
AI_SOURCE_DIRS = [
    ROOT / "app" / "dist-old-2" / "assets",
    ROOT / "app" / "dist" / "assets",
    ASSETS_DIR,
]

sys.path.insert(0, str(BACKEND_ROOT))

from app.config import settings  # noqa: E402
from app.storage.oss import _oss_client  # noqa: E402


def collect_asset_paths_from_seed() -> list[str]:
    data = json.loads(SEED_PATH.read_text(encoding="utf-8"))
    return sorted(set(re.findall(r"/assets/[\w.-]+\.jpg", json.dumps(data))))


def _resolve_local_file(filename: str) -> Path:
    """优先使用 dist-old-2 中的 AI 原图（>10KB），避免误用占位图。"""
    for folder in AI_SOURCE_DIRS:
        candidate = folder / filename
        if candidate.is_file() and candidate.stat().st_size > 10_000:
            return candidate
    fallback = ASSETS_DIR / filename
    if fallback.is_file():
        return fallback
    raise FileNotFoundError(
        f"找不到 AI 图片 {filename}，请先运行: python scripts/sync_ai_assets.py"
    )


def _has_ai_file(filename: str) -> bool:
    try:
        return _resolve_local_file(filename).stat().st_size > 10_000
    except FileNotFoundError:
        return False


def ensure_local_assets() -> None:
    """同步 AI 图到 public/assets 并校验 seed 所需的 jpg。"""
    needed = collect_asset_paths_from_seed()
    missing = [p for p in needed if not _has_ai_file(p.removeprefix("/assets/"))]
    if missing and SYNC_AI_SCRIPT.is_file():
        print("Syncing AI images from dist-old-2 ...")
        subprocess.run([sys.executable, str(SYNC_AI_SCRIPT)], check=True)
        missing = [p for p in needed if not _has_ai_file(p.removeprefix("/assets/"))]
    if missing:
        raise FileNotFoundError(
            f"缺少真实 AI 图片: {missing[:3]}... 请将原图放入 app/dist-old-2/assets/ 后重试"
        )
    print(f"Local AI assets OK ({len(needed)} files)")


def static_oss_key(filename: str) -> str:
    prefix = settings.oss_prefix
    if prefix and not prefix.endswith("/"):
        prefix += "/"
    return f"{prefix}assets/{filename}"


def public_url_for_key(key: str) -> str:
    return f"{settings.oss_public_base.rstrip('/')}/{key.lstrip('/')}"


def upload_all_seed_assets() -> dict[str, str]:
    """
    上传 seed 引用的全部 /assets/*.jpg 到 OSS。
    返回映射：/assets/foo.jpg → https://bucket.../rabbit/assets/foo.jpg
    """
    ensure_local_assets()
    client = _oss_client()
    bucket = settings.oss_bucket
    url_map: dict[str, str] = {}

    for asset_path in collect_asset_paths_from_seed():
        filename = asset_path.removeprefix("/assets/")
        local_file = _resolve_local_file(filename)
        key = static_oss_key(filename)
        client.put_object_from_file(
            oss.PutObjectRequest(bucket=bucket, key=key),
            str(local_file),
        )
        url_map[asset_path] = public_url_for_key(key)
        print(f"  OSS {key}")

    print(f"Uploaded {len(url_map)} assets to {settings.oss_bucket}")
    return url_map
