from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import BootstrapResponse, HealthResponse, SetCurrentBunnyPayload
from app.services.bootstrap import build_bootstrap, set_current_bunny_id

router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse()


@router.get("/bootstrap", response_model=BootstrapResponse)
def bootstrap(db: Session = Depends(get_db)) -> BootstrapResponse:
    return build_bootstrap(db)


@router.put("/settings/current-bunny")
def update_current_bunny(payload: SetCurrentBunnyPayload, db: Session = Depends(get_db)) -> dict[str, str]:
    try:
        set_current_bunny_id(db, payload.bunnyId)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return {"currentBunnyId": payload.bunnyId}
