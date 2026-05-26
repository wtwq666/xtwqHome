from typing import Literal

from pydantic import BaseModel, Field

HealthRecordType = Literal["checkup", "abnormal", "prevention", "care"]


class BunnySchema(BaseModel):
    id: str
    name: str
    breed: str
    birthDate: str
    avatar: str
    weight: int
    notes: str | None = None

    model_config = {"from_attributes": True}


class TimelineEventSchema(BaseModel):
    id: str
    date: str
    title: str
    coverImage: str
    description: str
    detailImages: list[str]
    mood: str
    color: str


class WeightRecordSchema(BaseModel):
    id: str
    date: str
    weight: int


class HealthRecordSchema(BaseModel):
    id: str
    date: str
    type: HealthRecordType
    description: str
    status: str


class PhotoSchema(BaseModel):
    id: str
    src: str
    date: str
    description: str
    year: int
    tags: list[str] = Field(default_factory=list)


class BunnyDataBundleSchema(BaseModel):
    bunny: BunnySchema
    timelineEvents: list[TimelineEventSchema]
    weightRecords: list[WeightRecordSchema]
    photos: list[PhotoSchema]
    healthRecords: list[HealthRecordSchema]


class BootstrapResponse(BaseModel):
    bunnies: list[BunnySchema]
    currentBunnyId: str
    bunnyData: dict[str, BunnyDataBundleSchema]


class HealthResponse(BaseModel):
    status: str = "ok"


class UploadResponse(BaseModel):
    url: str


class SetCurrentBunnyPayload(BaseModel):
    bunnyId: str


class CreateBunnyPayload(BaseModel):
    name: str
    breed: str
    birthDate: str
    weight: int
    avatar: str | None = "/assets/photo-11-baby.jpg"


class CreateTimelineEventPayload(BaseModel):
    bunnyId: str
    date: str
    title: str
    coverImage: str
    description: str
    detailImages: list[str]
    mood: str
    color: str


class UpdateTimelineEventPayload(BaseModel):
    date: str | None = None
    title: str | None = None
    coverImage: str | None = None
    description: str | None = None
    detailImages: list[str] | None = None
    mood: str | None = None
    color: str | None = None


class CreateWeightRecordPayload(BaseModel):
    bunnyId: str
    date: str
    weight: int


class UpdateWeightRecordPayload(BaseModel):
    date: str | None = None
    weight: int | None = None


class CreateHealthRecordPayload(BaseModel):
    bunnyId: str
    date: str
    type: HealthRecordType
    description: str
    status: str


class UpdateHealthRecordPayload(BaseModel):
    date: str | None = None
    type: HealthRecordType | None = None
    description: str | None = None
    status: str | None = None


class CreatePhotoPayload(BaseModel):
    bunnyId: str
    src: str
    date: str
    description: str
    year: int
    tags: list[str] | None = None


class UpdatePhotoPayload(BaseModel):
    src: str | None = None
    date: str | None = None
    description: str | None = None
    year: int | None = None
    tags: list[str] | None = None
