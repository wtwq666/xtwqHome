"""体重记录变更后，同步 bunnies.weight 为按 record_date 排序的最后一条。"""

from sqlalchemy.orm import Session

from app.models import Bunny, WeightRecord


def sync_bunny_weight(db: Session, bunny_id: str) -> None:
    bunny = db.get(Bunny, bunny_id)
    if not bunny:
        return
    records = (
        db.query(WeightRecord)
        .filter(WeightRecord.bunny_id == bunny_id)
        .order_by(WeightRecord.record_date.asc())
        .all()
    )
    if not records:
        return
    bunny.weight = records[-1].weight
    db.commit()
