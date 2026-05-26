"""检查当前 .env 指向的 PostgreSQL 库是否有表和数据。"""

import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_ROOT))

from sqlalchemy import inspect, text

from app.config import settings
from app.database import SessionLocal, engine

print("Database:", settings.sqlalchemy_database_url.split("@")[-1])
print("PG_DATABASE:", settings.pg_database)

insp = inspect(engine)
tables = insp.get_table_names(schema="public")
print("public schema tables:", tables or "(无表)")

db = SessionLocal()
try:
    rows = db.execute(
        text(
            """
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
              AND table_type = 'BASE TABLE'
            ORDER BY 1, 2
            """
        )
    ).fetchall()
    print("\nAll user tables:")
    for schema, name in rows:
        print(f"  {schema}.{name}")

    for t in ("bunnies", "timeline_events", "weight_records", "health_records", "photos", "app_settings"):
        try:
            n = db.execute(text(f"SELECT COUNT(*) FROM public.{t}")).scalar()
            print(f"  public.{t}: {n} rows")
        except Exception as e:
            print(f"  public.{t}: (不存在) {e.__class__.__name__}")
finally:
    db.close()
