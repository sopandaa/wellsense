from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.routes.auth import get_current_user  # adjust if different location
from sqlalchemy import func, desc
from datetime import date, timedelta
 


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




@router.get("/employee-risk/{employee_id}")
def employee_risk(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "HR":
        raise HTTPException(status_code=403, detail="Only HR can view employee risk")

    # Get last 7 days of records
    seven_days_ago = date.today() - timedelta(days=7)

    records = (
        db.query(models.WellnessRecord)
        .filter(
            models.WellnessRecord.employee_id == employee_id,
            models.WellnessRecord.date >= seven_days_ago
        )
        .order_by(desc(models.WellnessRecord.date))
        .all()
    )

    if not records:
        raise HTTPException(status_code=404, detail="No recent records found")

    # Compute averages
    fatigue_avg = sum(r.fatigue_score for r in records) / len(records)
    stress_avg = sum(r.stress_level for r in records) / len(records)
    sleep_avg = sum(r.sleep_hours for r in records) / len(records)
    productivity_avg = sum(r.productivity_score for r in records) / len(records)

    # Burnout scoring formula (rule-based V1)
    raw_score = (
        fatigue_avg * 0.35 +
        stress_avg * 0.35 -
        sleep_avg * 0.15 -
        productivity_avg * 0.15
    )

    burnout_score = max(0, min(100, raw_score * 10))

    # Simple trend detection (compare last 3 vs first 3 days)
    first_half = records[-3:]
    last_half = records[:3]

    first_avg = sum(r.fatigue_score for r in first_half) / len(first_half)
    last_avg = sum(r.fatigue_score for r in last_half) / len(last_half)

    trend = "RISING" if last_avg > first_avg else "DECLINING"

    # Risk level classification
    if burnout_score < 40:
        risk_level = "LOW"
    elif burnout_score < 70:
        risk_level = "MODERATE"
    else:
        risk_level = "HIGH"

    return {
        "employee_id": employee_id,
        "burnout_score": round(burnout_score, 2),
        "risk_level": risk_level,
        "trend": trend,
        "drivers": {
            "fatigue_avg": round(fatigue_avg, 2),
            "stress_avg": round(stress_avg, 2),
            "sleep_avg": round(sleep_avg, 2),
            "productivity_avg": round(productivity_avg, 2)
        }
    }