"""
清空 tutusys 业务表 → 建表 v2 → 灌 seed → 同步 AI 图到 OSS 并更新 RDS URL。

警告：会删除当前库中全部业务数据！
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent.parent
ROOT = BACKEND_ROOT.parent
sys.path.insert(0, str(BACKEND_ROOT))

from app.config import settings  # noqa: E402
from app.database import Base, engine, import_models  # noqa: E402

import_models()


def main() -> None:
    db_label = settings.sqlalchemy_database_url.split("@")[-1]
    print("=" * 60)
    print("reset_and_seed — 将清空并重建数据库")
    print(f"Target: {db_label}")
    print("=" * 60)

    print("\n[1/4] DROP + CREATE tables (schema v2)...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("  Tables:", ", ".join(sorted(Base.metadata.tables.keys())))

    print("\n[2/4] Seed initial data...")
    from scripts.seed import main as seed_main  # noqa: E402

    seed_main()

    sync_script = ROOT / "scripts" / "sync_ai_assets.py"
    if sync_script.is_file():
        print("\n[3/4] Sync AI images to public/assets...")
        subprocess.run([sys.executable, str(sync_script)], check=True)
    else:
        print("\n[3/4] Skip sync_ai_assets (script missing)")

    print("\n[4/4] Upload to OSS + update RDS URLs...")
    from scripts.migrate_asset_urls import apply_url_map  # noqa: E402
    from scripts.oss_assets import upload_all_seed_assets  # noqa: E402

    url_map = upload_all_seed_assets()
    n = apply_url_map(url_map)
    print(f"  Updated {n} image URL fields in RDS")

    print("\nDone. Restart uvicorn and refresh the browser.")


if __name__ == "__main__":
    main()
