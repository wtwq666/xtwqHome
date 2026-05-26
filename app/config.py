from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(BACKEND_ROOT / ".env", override=False)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BACKEND_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- PostgreSQL（优先）或显式 DATABASE_URL ---
    pg_host: str = ""
    pg_port: int = 5432
    pg_database: str = "tutu"
    pg_user: str = ""
    pg_password: str = ""
    database_url: str = ""

    upload_dir: str = str(BACKEND_ROOT / "uploads")
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    # local | oss
    storage_backend: str = "local"
    oss_bucket: str = "coucou-oss"
    oss_region: str = "cn-guangzhou"
    oss_prefix: str = "rabbit/"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def sqlalchemy_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        if self.pg_host and self.pg_user:
            pwd = quote_plus(self.pg_password)
            return (
                f"postgresql+psycopg2://{self.pg_user}:{pwd}"
                f"@{self.pg_host}:{self.pg_port}/{self.pg_database}"
            )
        return f"sqlite:///{(BACKEND_ROOT / 'data' / 'bunny.db').as_posix()}"

    @property
    def is_sqlite(self) -> bool:
        return self.sqlalchemy_database_url.startswith("sqlite")

    @property
    def oss_endpoint_host(self) -> str:
        return f"oss-{self.oss_region}.aliyuncs.com"

    @property
    def oss_public_base(self) -> str:
        """https://bucket.oss-cn-guangzhou.aliyuncs.com"""
        return f"https://{self.oss_bucket}.{self.oss_endpoint_host}"

    def oss_key(self, filename: str) -> str:
        prefix = self.oss_prefix
        if prefix and not prefix.endswith("/"):
            prefix += "/"
        return f"{prefix}{filename}"


settings = Settings()
if settings.is_sqlite:
    Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
    (BACKEND_ROOT / "data").mkdir(parents=True, exist_ok=True)


def get_upload_dir() -> Path:
    return Path(settings.upload_dir)
