from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.routes.auth import get_current_user  # adjust if different location
from sqlalchemy import func, desc
from datetime import date, timedelta

from app.services.burnout_service import calculate_burnout
from collections import defaultdict


router = APIRouter(prefix="/wellness", tags=["Wellness"])


# -----------------------------
# TOP 5 HIGH RISK EMPLOYEES
# -----------------------------
@router.get("/employee-risk")
def employee_risk(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    if current_user.role != "HR":
        raise HTTPException(status_code=403, detail="Only HR can view employee risk")

    employees = db.query(models.User).filter(
        models.User.company_id == current_user.company_id,
        models.User.role == "employee"
    ).all()

    results = []

    for employee in employees:

        records = (
            db.query(models.WellnessRecord)
            .filter(models.WellnessRecord.employee_id == employee.id)
            .order_by(desc(models.WellnessRecord.date))
            .limit(7)
            .all()
        )

        result = calculate_burnout(records)

        if not result:
            continue

        score, risk = result

        results.append({
            "employee_id": employee.id,
            "name": employee.email,
            "department": employee.department,
            "burnout_score": score,
            "risk_level": risk
        })

    results.sort(key=lambda x: x["burnout_score"], reverse=True)

    return results


# -----------------------------
# DEPARTMENT RISK
# -----------------------------
@router.get("/department-risk")
def department_risk(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    if current_user.role != "HR":
        raise HTTPException(status_code=403)

    employees = db.query(models.User).filter(
        models.User.company_id == current_user.company_id,
        models.User.role == "employee"
    ).all()

    department_data = {}

    for employee in employees:

        records = db.query(models.WellnessRecord).filter(
            models.WellnessRecord.employee_id == employee.id
        ).order_by(models.WellnessRecord.date.desc()).limit(7).all()

        result = calculate_burnout(records)

        if not result:
            continue

        score, _ = result

        dept = employee.department

        if dept not in department_data:
            department_data[dept] = {
                "scores": [],
                "employee_count": 0
            }

        department_data[dept]["scores"].append(score)
        department_data[dept]["employee_count"] += 1

    response = []

    for dept, data in department_data.items():

        avg_score = sum(data["scores"]) / len(data["scores"])

        if avg_score < 35:
            risk = "LOW"
        elif avg_score < 65:
            risk = "MODERATE"
        else:
            risk = "HIGH"

        response.append({
            "department": dept,
            "avg_burnout": round(avg_score, 2),
            "risk_level": risk,
            "employee_count": data["employee_count"]
        })

    return response

# -----------------------------
# COMPANY TREND
# -----------------------------
@router.get("/company-trend")
def company_trend(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    if current_user.role != "HR":
        raise HTTPException(status_code=403, detail="Only HR can view company trend")

    employees = db.query(models.User).filter(
        models.User.company_id == current_user.company_id,
        models.User.role == "employee"
    ).all()

    employee_ids = [e.id for e in employees]

    records = db.query(models.WellnessRecord).filter(
        models.WellnessRecord.employee_id.in_(employee_ids)
    ).all()

    date_scores = defaultdict(list)

    for record in records:

        result = calculate_burnout([record])

        if not result:
            continue

        score, _ = result

        date_scores[str(record.date)].append(score)

    trend = []

    for d, scores in date_scores.items():
        trend.append({
            "date": d,
            "burnout": round(sum(scores) / len(scores), 2)
        })

    trend.sort(key=lambda x: x["date"])

    return trend


# -----------------------------
# RISK DISTRIBUTION
# -----------------------------
@router.get("/risk-distribution")
def risk_distribution(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    if current_user.role != "HR":
        raise HTTPException(status_code=403, detail="Only HR can view risk distribution")

    employees = db.query(models.User).filter(
        models.User.company_id == current_user.company_id,
        models.User.role == "employee"
    ).all()

    distribution = {
        "LOW": 0,
        "MODERATE": 0,
        "HIGH": 0
    }

    for employee in employees:

        records = (
            db.query(models.WellnessRecord)
            .filter(models.WellnessRecord.employee_id == employee.id)
            .order_by(desc(models.WellnessRecord.date))
            .limit(7)
            .all()
        )

        result = calculate_burnout(records)

        if not result:
            continue

        score, risk = result

        distribution[risk] += 1

    return distribution


# -----------------------------
# EMPLOYEE PROFILE
# -----------------------------
@router.get("/employee-risk/{employee_id}")
def employee_profile(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    records = (
        db.query(models.WellnessRecord)
        .filter(models.WellnessRecord.employee_id == employee_id)
        .order_by(desc(models.WellnessRecord.date))
        .limit(7)
        .all()
    )

    if not records:
        return {
            "employee_id": employee_id,
            "burnout_score": 0,
            "risk_level": "LOW"
        }

    score, risk = calculate_burnout(records)

    return {
        "employee_id": employee_id,
        "burnout_score": score,
        "risk_level": risk
    }


# -----------------------------
# EMPLOYEE TREND
# -----------------------------
@router.get("/employee-trend/{employee_id}")
def employee_trend(
    employee_id: int,
    db: Session = Depends(get_db),
):

    records = (
        db.query(models.WellnessRecord)
        .filter(models.WellnessRecord.employee_id == employee_id)
        .order_by(models.WellnessRecord.date)
        .all()
    )

    trend = []

    for r in records:

        result = calculate_burnout([r])

        if not result:
            continue

        score, _ = result

        trend.append({
            "date": str(r.date),
            "burnout": score
        })

    return trend




  

@router.get("/ai-insights")
def ai_insights(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    insights = []
    recommendations = []

    today = date.today()
    seven_days_ago = today - timedelta(days=7)

    employees = db.query(models.User).filter(
        models.User.company_id == current_user.company_id,
        models.User.role == "employee"
    ).all()

    low_sleep = 0
    long_hours = 0
    high_fatigue = 0
    low_productivity = 0
    high_burnout = 0

    department_scores = {}

    for employee in employees:

        records = db.query(models.WellnessRecord).filter(
            models.WellnessRecord.employee_id == employee.id,
            models.WellnessRecord.date >= seven_days_ago
        ).order_by(models.WellnessRecord.date).all()

        if not records:
            continue

        avg_sleep = sum(r.sleep_hours for r in records) / len(records)
        avg_hours = sum(r.work_hours for r in records) / len(records)
        avg_fatigue = sum(r.fatigue_score for r in records) / len(records)
        avg_productivity = sum(r.productivity_score for r in records) / len(records)

        # Employee level indicators
        if avg_sleep < 6:
            low_sleep += 1

        if avg_hours > 9:
            long_hours += 1

        if avg_fatigue > 7:
            high_fatigue += 1

        if avg_productivity < 4:
            low_productivity += 1

        # Burnout score
        burnout_score = (
            (10 - avg_sleep) * 2 +
            avg_hours * 1.5 +
            avg_fatigue * 2 +
            (10 - avg_productivity) * 1.5
        )

        if burnout_score > 70:
            high_burnout += 1

        # Department aggregation
        dept = employee.department

        if dept not in department_scores:
            department_scores[dept] = []

        department_scores[dept].append(burnout_score)

        # Trend detection (last record vs first record)
        if len(records) >= 2:
            first = records[0]
            last = records[-1]

            if last.fatigue_score > first.fatigue_score + 2:
                insights.append(
                    f"Increasing fatigue trend detected for employees in {dept} department."
                )

            if last.sleep_hours < first.sleep_hours - 1:
                insights.append(
                    f"Sleep reduction trend observed in {dept} department."
                )

    # General insights
    if low_sleep:
        insights.append(f"{low_sleep} employees averaging less than 6 hours of sleep.")

    if long_hours:
        insights.append(f"{long_hours} employees consistently working more than 9 hours daily.")

    if high_fatigue:
        insights.append(f"{high_fatigue} employees reporting high fatigue levels.")

    if low_productivity:
        insights.append(f"{low_productivity} employees showing declining productivity.")

    if high_burnout:
        insights.append(f"{high_burnout} employees at high burnout risk.")

    # Department burnout insights
    for dept, scores in department_scores.items():

        avg_score = sum(scores) / len(scores)

        if avg_score > 70:
            insights.append(f"{dept} department showing severe burnout risk.")

        elif avg_score > 50:
            insights.append(f"{dept} department experiencing moderate stress levels.")

    # HR recommendations
    if low_sleep > 0:
        recommendations.append(
            "Encourage better work-life balance and discourage late-night work."
        )

    if long_hours > 0:
        recommendations.append(
            "Review workload distribution to reduce excessive working hours."
        )

    if high_fatigue > 0:
        recommendations.append(
            "Promote short breaks and mental health support programs."
        )

    if high_burnout > 0:
        recommendations.append(
            "Consider wellness initiatives or counseling for high-risk employees."
        )

    if not insights:
        insights.append("Employee wellness trends appear stable this week.")

    return {
        "insights": insights,
        "recommendations": recommendations
    }