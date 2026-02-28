from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.routes.auth import get_current_user  # adjust if different location


print("WELLNESS FILE LOADED")


router = APIRouter(
    prefix="/wellness",
    tags=["Wellness"]
)

@router.post("/", response_model=schemas.WellnessResponse)
def submit_wellness(
    data: schemas.WellnessCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "employee":
        raise HTTPException(status_code=403, detail="Only employees can submit wellness data")

    record = models.WellnessRecord(
        employee_id=current_user.id,
        work_hours=data.work_hours,
        fatigue_score=data.fatigue_score,
        stress_level=data.stress_level,
        sleep_hours=data.sleep_hours,
        productivity_score=data.productivity_score
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record
