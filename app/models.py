import json
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class AppSetting(Base):
    __tablename__ = "app_settings"

    key: Mapped[str] = mapped_column(String(64), primary_key=True)
    value: Mapped[str] = mapped_column(String(256))


class Bunny(Base):
    __tablename__ = "bunnies"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    breed: Mapped[str] = mapped_column(String(128))
    birth_date: Mapped[str] = mapped_column(String(16))
    avatar_path: Mapped[str] = mapped_column(String(512))
    weight: Mapped[int] = mapped_column(Integer)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow
    )

    timeline_events: Mapped[list["TimelineEvent"]] = relationship(
        back_populates="bunny", cascade="all, delete-orphan"
    )
    weight_records: Mapped[list["WeightRecord"]] = relationship(
        back_populates="bunny", cascade="all, delete-orphan"
    )
    photos: Mapped[list["Photo"]] = relationship(back_populates="bunny", cascade="all, delete-orphan")
    health_records: Mapped[list["HealthRecord"]] = relationship(
        back_populates="bunny", cascade="all, delete-orphan"
    )


class TimelineEvent(Base):
    __tablename__ = "timeline_events"
    __table_args__ = (Index("ix_timeline_bunny_date", "bunny_id", "event_date"),)

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    bunny_id: Mapped[str] = mapped_column(String(64), ForeignKey("bunnies.id", ondelete="CASCADE"))
    event_date: Mapped[str] = mapped_column(String(16))
    title: Mapped[str] = mapped_column(String(256))
    cover_image_path: Mapped[str] = mapped_column(String(512))
    description: Mapped[str] = mapped_column(Text)
    detail_images_json: Mapped[str] = mapped_column(Text, default="[]")
    mood: Mapped[str] = mapped_column(String(32))
    color: Mapped[str] = mapped_column(String(16))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow
    )

    bunny: Mapped["Bunny"] = relationship(back_populates="timeline_events")

    @property
    def detail_images(self) -> list[str]:
        return json.loads(self.detail_images_json or "[]")

    @detail_images.setter
    def detail_images(self, value: list[str]) -> None:
        self.detail_images_json = json.dumps(value[:9])


class WeightRecord(Base):
    __tablename__ = "weight_records"
    __table_args__ = (
        UniqueConstraint("bunny_id", "record_date", name="uq_weight_bunny_date"),
        Index("ix_weight_bunny_date", "bunny_id", "record_date"),
    )

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    bunny_id: Mapped[str] = mapped_column(String(64), ForeignKey("bunnies.id", ondelete="CASCADE"))
    record_date: Mapped[str] = mapped_column(String(16))
    weight: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow
    )

    bunny: Mapped["Bunny"] = relationship(back_populates="weight_records")


class HealthRecord(Base):
    __tablename__ = "health_records"
    __table_args__ = (Index("ix_health_bunny_date", "bunny_id", "record_date"),)

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    bunny_id: Mapped[str] = mapped_column(String(64), ForeignKey("bunnies.id", ondelete="CASCADE"))
    record_date: Mapped[str] = mapped_column(String(16))
    type: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow
    )

    bunny: Mapped["Bunny"] = relationship(back_populates="health_records")


class Photo(Base):
    __tablename__ = "photos"
    __table_args__ = (Index("ix_photo_bunny_date", "bunny_id", "photo_date"),)

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    bunny_id: Mapped[str] = mapped_column(String(64), ForeignKey("bunnies.id", ondelete="CASCADE"))
    src_path: Mapped[str] = mapped_column(String(512))
    photo_date: Mapped[str] = mapped_column(String(16))
    description: Mapped[str] = mapped_column(Text, default="")
    year: Mapped[int] = mapped_column(Integer)
    tags_json: Mapped[str] = mapped_column(Text, default="[]")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow
    )

    bunny: Mapped["Bunny"] = relationship(back_populates="photos")

    @property
    def tags(self) -> list[str]:
        return json.loads(self.tags_json or "[]")

    @tags.setter
    def tags(self, value: list[str]) -> None:
        self.tags_json = json.dumps(value)
