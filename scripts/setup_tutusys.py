"""
一键初始化 tutusys 库：
  1. 建表
  2. 导入 initial_seed.json 到 PostgreSQL
  3. 上传 Mock/占位图到 OSS
  4. 把库内 /assets/ 路径改为 OSS HTTPS URL

用法（在 backend 目录）:
  python scripts/setup_tutusys.py
"""

from __future__ import annotations

import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_ROOT))

from app.config import settings  # noqa: E402
from app.database import Base, engine, import_models  # noqa: E402

import_models()
from scripts.migrate_asset_urls import apply_url_map  # noqa: E402
from scripts.oss_assets import upload_all_seed_assets  # noqa: E402
from scripts.seed import _load, _wipe  # noqa: E402
from scripts.seed import SEED_PATH  # noqa: E402
import json  # noqa: E402
from app.database import SessionLocal  # noqa: E402


def main() -> None:
    db_label = settings.sqlalchemy_database_url.split("@")[-1]
    print("=" * 60)
    print("臭臭的家 — tutusys 全量初始化")
    print(f"Database: {db_label}")
    print(f"OSS: {settings.oss_bucket} / {settings.oss_prefix}assets/")
    print("=" * 60)

    if settings.pg_database != "tutusys" and "tutusys" not in db_label:
        print(
            f"Warning: PG_DATABASE={settings.pg_database!r}, expected 'tutusys'. "
            "Check backend/.env"
        )

    print("\n[1/4] Create tables...")
    Base.metadata.create_all(bind=engine)

    print("\n[2/4] Seed PostgreSQL from initial_seed.json...")
    data = json.loads(SEED_PATH.read_text(encoding="utf-8"))
    db = SessionLocal()
    try:
        _wipe(db)
        _load(db, data)
    finally:
        db.close()
    print(f"  -> {len(data['bunnies'])} bunnies loaded")

    print("\n[3/4] Sync AI images + upload to OSS...")
    import subprocess
    import sys as _sys
    from pathlib import Path as _Path

    sync_script = _Path(__file__).resolve().parent.parent.parent / "scripts" / "sync_ai_assets.py"
    if sync_script.is_file():
        subprocess.run([_sys.executable, str(sync_script)], check=True)
    url_map = upload_all_seed_assets()

    print("\n[4/4] Update RDS image paths to OSS URLs...")
    n = apply_url_map(url_map)
    print(f"  -> {n} fields updated")

    print("\nDone.")
    print("Restart uvicorn, then open http://localhost:3000")
    print("Sample OSS URL:", next(iter(url_map.values()), "(none)"))


if __name__ == "__main__":
    main()
