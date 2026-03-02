from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.routes.auth import get_current_user  # adjust if different location
from sqlalchemy import func

 


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






@router.get("/company-summary")
def company_summary(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "HR":
        raise HTTPException(status_code=403, detail="Only HR can view company summary")

    result = (
        db.query(
            func.avg(models.WellnessRecord.fatigue_score),
            func.avg(models.WellnessRecord.stress_level),
            func.avg(models.WellnessRecord.sleep_hours),
            func.avg(models.WellnessRecord.productivity_score),
            func.count(models.WellnessRecord.id),
        )
        .join(models.User, models.User.id == models.WellnessRecord.employee_id)
        .filter(models.User.company_id == current_user.company_id)
        .first()
    )

    return {
        "avg_fatigue": float(result[0] or 0),
        "avg_stress": float(result[1] or 0),
        "avg_sleep": float(result[2] or 0),
        "avg_productivity": float(result[3] or 0),
        "total_records": result[4] or 0
    }