# 臭臭的家 — FastAPI 后端（Phase 4）

对齐 [`docs/api-contract.md`](../docs/api-contract.md) v1.0。

## 快速开始

```powershell
cd backend
pip install -r requirements.txt
python scripts/init_database.py --seed   # 新库：建表 + 初始数据
uvicorn app.main:app --reload --port 8000
```

新建 RDS 库名与切换步骤见 [`docs/new-database-setup.md`](../docs/new-database-setup.md)。

另开终端启动前端（`app/`，`VITE_USE_MOCK=false` 时走代理）。

## 测试

```powershell
cd backend
.\scripts\run_tests.ps1
# 或
pytest -v
```

## 环境变量（`backend/.env`，勿提交 Git）

| 变量 | 说明 |
|------|------|
| `PG_HOST` / `PG_PORT` / `PG_DATABASE` / `PG_USER` / `PG_PASSWORD` | 阿里云 RDS PostgreSQL |
| `OSS_ACCESS_KEY_ID` / `OSS_ACCESS_KEY_SECRET` | RAM 凭证（OSS SDK 自动读取） |
| `STORAGE_BACKEND` | `oss` 或 `local` |
| `OSS_BUCKET` / `OSS_REGION` / `OSS_PREFIX` | 如 `coucou-oss`、`cn-guangzhou`、`rabbit/` |
| `CORS_ORIGINS` | 逗号分隔前端地址 |

未配置 `PG_HOST` 时回退 SQLite `data/bunny.db`。

## 目录

- `app/` — FastAPI、SQLAlchemy、路由
- `scripts/seed.py` — 从 `initial_seed.json` 灌库（与前端 `initialBootstrap.ts` 一致）
- `tests/test_api.py` — 契约 API 测试
- `uploads/`、`data/` — 本地数据（已 gitignore）
