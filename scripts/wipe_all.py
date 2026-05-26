"""
清空 tutusys 全部业务表 + 删除 OSS 上 rabbit/ 前缀下的所有对象。

警告：不可恢复。清空后需运行 reset_and_seed.py 才能再次使用应用。

用法（backend 目录）:
  python scripts/wipe_all.py
  python scripts/wipe_all.py --yes   # 跳过确认
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import alibabacloud_oss_v2 as oss

BACKEND_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_ROOT))

from app.config import settings  # noqa: E402
from app.database import Base, engine, import_models  # noqa: E402
from app.storage.oss import _oss_client  # noqa: E402


def _oss_prefix() -> str:
    prefix = settings.oss_prefix or ""
    if prefix and not prefix.endswith("/"):
        prefix += "/"
    return prefix


def wipe_database(*, recreate_schema: bool = True) -> list[str]:
    import_models()
    tables = sorted(Base.metadata.tables.keys())
    Base.metadata.drop_all(bind=engine)
    if recreate_schema:
        Base.metadata.create_all(bind=engine)
    return tables


def wipe_oss() -> int:
    prefix = _oss_prefix()
    if not prefix:
        print("  OSS_PREFIX empty, skip.")
        return 0

    client = _oss_client()
    bucket = settings.oss_bucket
    keys: list[str] = []
    paginator = client.list_objects_v2_paginator()

    for page in paginator.iter_page(
        oss.ListObjectsV2Request(bucket=bucket, prefix=prefix)
    ):
        if page.contents:
            keys.extend(obj.key for obj in page.contents if obj.key)

    if not keys:
        return 0

    deleted = 0
    batch_size = 1000
    for i in range(0, len(keys), batch_size):
        batch = keys[i : i + batch_size]
        result = client.delete_multiple_objects(
            oss.DeleteMultipleObjectsRequest(
                bucket=bucket,
                objects=[oss.DeleteObject(key=k) for k in batch],
            )
        )
        deleted += len(result.deleted_objects or batch)

    return deleted


def main() -> None:
    parser = argparse.ArgumentParser(description="Wipe RDS tables and OSS rabbit/ prefix")
    parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation")
    args = parser.parse_args()

    db_label = settings.sqlalchemy_database_url.split("@")[-1]
    oss_label = f"{settings.oss_bucket} / {_oss_prefix()}*"

    print("=" * 60)
    print("wipe_all — 将清空数据库并删除 OSS 对象")
    print(f"  Database: {db_label}")
    print(f"  OSS:      {oss_label}")
    print("=" * 60)

    if not args.yes:
        answer = input("\n确认继续？输入 yes 执行: ").strip().lower()
        if answer != "yes":
            print("已取消。")
            return

    print("\n[1/2] DROP all tables + recreate empty schema...")
    tables = wipe_database()
    if tables:
        print(f"  Tables: {', '.join(tables)} (0 rows)")
    else:
        print("  (no tables registered)")

    print("\n[2/2] Delete OSS objects...")
    try:
        n = wipe_oss()
        print(f"  Deleted {n} object(s) under {_oss_prefix()}")
    except Exception as e:
        print(f"  OSS error: {e}")
        raise

    print("\nDone. Database has empty tables; OSS prefix is clear.")
    print("To load demo data: python scripts/reset_and_seed.py")


if __name__ == "__main__":
    main()
