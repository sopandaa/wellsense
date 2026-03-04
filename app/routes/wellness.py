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

    # --- Feature Engineering ---
    fatigue_avg = sum(r.fatigue_score for r in records) / len(records)
    stress_avg = sum(r.stress_level for r in records) / len(records)
    sleep_avg = sum(r.sleep_hours for r in records) / len(records)
    productivity_avg = sum(r.productivity_score for r in records) / len(records)

    # --- Normalize to 0–1 ---
    fatigue_norm = fatigue_avg / 10
    stress_norm = stress_avg / 10
    sleep_norm = sleep_avg / 8  # assuming 8 hrs ideal
    productivity_norm = productivity_avg / 10

    # --- Burnout Score (Clean Formula) ---
    burnout_score = (
        fatigue_norm * 0.35 +
        stress_norm * 0.35 +
        (1 - sleep_norm) * 0.15 +
        (1 - productivity_norm) * 0.15
    ) * 100

    burnout_score = max(0, min(100, burnout_score))

    # --- Improved Trend Detection ---
    first_half = records[-3:]
    last_half = records[:3]

    fatigue_trend = (
        sum(r.fatigue_score for r in last_half) / len(last_half)
        >
        sum(r.fatigue_score for r in first_half) / len(first_half)
    )

    stress_trend = (
        sum(r.stress_level for r in last_half) / len(last_half)
        >
        sum(r.stress_level for r in first_half) / len(first_half)
    )

    sleep_trend = (
        sum(r.sleep_hours for r in last_half) / len(last_half)
        <
        sum(r.sleep_hours for r in first_half) / len(first_half)
    )

    worsening_signals = sum([fatigue_trend, stress_trend, sleep_trend])

    if worsening_signals >= 2:
        trend = "RISING"
    elif worsening_signals == 1:
        trend = "STABLE"
    else:
        trend = "DECLINING"

    # --- Risk Classification ---
    if burnout_score < 35:
        risk_level = "LOW"
    elif burnout_score < 65:
        risk_level = "MODERATE"
    else:
        risk_level = "HIGH"

    return {
        "employee_id": employee_id,
        "burnout_score": round(burnout_score, 2),
        "risk_level": risk_level,
        "trend": trend,
        "signals": {
            "fatigue_avg": round(fatigue_avg, 2),
            "stress_avg": round(stress_avg, 2),
            "sleep_avg": round(sleep_avg, 2),
            "productivity_avg": round(productivity_avg, 2)
        }
    }


@router.get("/employee-risk")
def all_employee_risk(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "HR":
        raise HTTPException(status_code=403, detail="Only HR can view employee risk")

    # Get all employees in same company
    employees = db.query(models.User).filter(
        models.User.company_id == current_user.company_id,
        models.User.role == "employee"
    ).all()

    results = []

    for employee in employees:
        seven_days_ago = date.today() - timedelta(days=7)

        records = (
            db.query(models.WellnessRecord)
            .filter(
                models.WellnessRecord.employee_id == employee.id,
                models.WellnessRecord.date >= seven_days_ago
            )
            .order_by(desc(models.WellnessRecord.date))
            .all()
        )

        if not records:
            continue

        fatigue_avg = sum(r.fatigue_score for r in records) / len(records)
        stress_avg = sum(r.stress_level for r in records) / len(records)
        sleep_avg = sum(r.sleep_hours for r in records) / len(records)
        productivity_avg = sum(r.productivity_score for r in records) / len(records)

        fatigue_norm = fatigue_avg / 10
        stress_norm = stress_avg / 10
        sleep_norm = sleep_avg / 8
        productivity_norm = productivity_avg / 10

        burnout_score = (
            fatigue_norm * 0.35 +
            stress_norm * 0.35 +
            (1 - sleep_norm) * 0.15 +
            (1 - productivity_norm) * 0.15
        ) * 100

        burnout_score = max(0, min(100, burnout_score))

        if burnout_score < 35:
            risk_level = "LOW"
        elif burnout_score < 65:
            risk_level = "MODERATE"
        else:
            risk_level = "HIGH"

        results.append({
            "employee_id": employee.id,
            "name": employee.email,  # change to employee.name if you have it
            "department": employee.department,
            "burnout_score": round(burnout_score, 2),
            "risk_level": risk_level
        })

    return results



@router.get("/department-risk")
def department_risk(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "HR":
        raise HTTPException(status_code=403, detail="Only HR can view department risk")

    # Get all employees in HR's company
    employees = (
        db.query(models.User)
        .filter(
            models.User.company_id == current_user.company_id,
            models.User.role.ilike("employee")
        )
        .all()
    )

    if not employees:
        return []

    department_data = {}

    for employee in employees:
        records = (
            db.query(models.WellnessRecord)
            .filter(models.WellnessRecord.employee_id == employee.id)
            .order_by(models.WellnessRecord.date.desc())
            .limit(7)
            .all()
        )

        if not records:
            continue

        fatigue_avg = sum(r.fatigue_score for r in records) / len(records)
        stress_avg = sum(r.stress_level for r in records) / len(records)
        sleep_avg = sum(r.sleep_hours for r in records) / len(records)
        productivity_avg = sum(r.productivity_score for r in records) / len(records)

        # Normalize
        fatigue_norm = fatigue_avg / 10
        stress_norm = stress_avg / 10
        sleep_norm = sleep_avg / 8
        productivity_norm = productivity_avg / 10

        burnout_score = (
            fatigue_norm * 0.35 +
            stress_norm * 0.35 +
            (1 - sleep_norm) * 0.15 +
            (1 - productivity_norm) * 0.15
        ) * 100

        burnout_score = max(0, min(100, burnout_score))

        dept = employee.department or "Unassigned"

        if dept not in department_data:
            department_data[dept] = {
                "total_score": 0,
                "count": 0
            }

        department_data[dept]["total_score"] += burnout_score
        department_data[dept]["count"] += 1

    # Build response
    response = []

    for dept, values in department_data.items():
        avg_score = values["total_score"] / values["count"]

        if avg_score < 35:
            risk_level = "LOW"
        elif avg_score < 65:
            risk_level = "MODERATE"
        else:
            risk_level = "HIGH"

        response.append({
            "department": dept,
            "avg_burnout_score": round(avg_score, 2),
            "risk_level": risk_level,
            "employee_count": values["count"]
        })
 
    return response
    




@router.get("/company-trend")
def get_company_trend(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    records = (
        db.query(models.WellnessRecord)
        .join(models.User)
        .filter(models.User.company_id == current_user.company_id)
        .all()
    )

    daily_data = {}

    for record in records:
        burnout = (
            record.fatigue_score * 0.3 +
            record.stress_level * 0.3 +
            (10 - record.sleep_hours) * 0.2 +
            (10 - record.productivity_score) * 0.2
        )

        date_str = record.date.strftime("%Y-%m-%d")

        if date_str not in daily_data:
            daily_data[date_str] = []

        daily_data[date_str].append(burnout)

    result = []

    for date, scores in daily_data.items():
        avg_burnout = sum(scores) / len(scores)
        result.append({
            "date": date,
            "avg_burnout": round(avg_burnout, 2)
        })

    result.sort(key=lambda x: x["date"])

    return result




@router.get("/risk-distribution")
def get_risk_distribution(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    employees = (
        db.query(models.User)
        .filter(
            models.User.company_id == current_user.company_id,
            models.User.role == "employee"
        )
        .all()
    )

    distribution = {
        "LOW": 0,
        "MODERATE": 0,
        "HIGH": 0
    }

    for employee in employees:
        records = (
            db.query(models.WellnessRecord)
            .filter(models.WellnessRecord.employee_id == employee.id)
            .order_by(models.WellnessRecord.date.desc())
            .limit(7)
            .all()
        )

        if not records:
            continue

        avg_fatigue = sum(r.fatigue_score for r in records) / len(records)
        avg_stress = sum(r.stress_level for r in records) / len(records)
        avg_sleep = sum(r.sleep_hours for r in records) / len(records)
        avg_productivity = sum(r.productivity_score for r in records) / len(records)

        burnout = (
            avg_fatigue * 0.3 +
            avg_stress * 0.3 +
            (10 - avg_sleep) * 0.2 +
            (10 - avg_productivity) * 0.2
        )

        if burnout >= 7:
            distribution["HIGH"] += 1
        elif burnout >= 4:
            distribution["MODERATE"] += 1
        else:
            distribution["LOW"] += 1

    return distribution