"""在新 PostgreSQL 库中创建表结构；可选导入 initial_seed.json。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_ROOT))

from app.config import settings  # noqa: E402
from app.database import Base, engine  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize PostgreSQL schema for 臭臭的家")
    parser.add_argument(
        "--seed",
        action="store_true",
        help="建表后执行 seed.py 写入初始示例数据",
    )
    args = parser.parse_args()

    db_label = settings.sqlalchemy_database_url.split("@")[-1]
    print(f"Target database: {db_label}")

    if settings.is_sqlite:
        print("Warning: PG_HOST not set, using SQLite. Set PG_* in .env for RDS.")

    Base.metadata.create_all(bind=engine)
    tables = sorted(Base.metadata.tables.keys())
    print(f"Created {len(tables)} tables: {', '.join(tables)}")

    if args.seed:
        from scripts.seed import main as seed_main  # noqa: E402

        print("Running seed...")
        seed_main()
    else:
        print("Done. Run with --seed to load initial data, or: python scripts/seed.py")


if __name__ == "__main__":
    main()
