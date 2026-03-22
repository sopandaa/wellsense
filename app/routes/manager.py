from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.routes.auth import get_current_user
from app import models
from app.services.burnout_service import calculate_burnout
from sqlalchemy import desc
from datetime import date, timedelta

from app.services.heatmap_service import get_status_from_burnout
from app.models import User, WellnessRecord

from collections import defaultdict



router = APIRouter(prefix="/manager", tags=["Manager"])


def require_manager(user: models.User = Depends(get_current_user)):
    if user.role != "MANAGER":
        raise HTTPException(status_code=403, detail="Managers only")
    return user


@router.get("/team")
def get_team(
    db: Session = Depends(get_db),
    manager: models.User = Depends(require_manager)
):

    team = db.query(models.User).filter(
        models.User.manager_id == manager.id
    ).all()

    return team


@router.get("/team-risk")
def team_risk(
    db: Session = Depends(get_db),
    manager: models.User = Depends(require_manager)
):

    team = db.query(models.User).filter(
        models.User.manager_id == manager.id
    ).all()

    results = []

    for employee in team:

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
            "name": employee.name,
            "burnout_score": score,
            "risk_level": risk
        })

    return results



@router.get("/team-risk")
def team_risk(
    db: Session = Depends(get_db),
    manager: models.User = Depends(require_manager)
):

    team = db.query(models.User).filter(
        models.User.manager_id == manager.id
    ).all()

    results = []

    for employee in team:

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
            "name": employee.name,
            "burnout_score": score,
            "risk_level": risk
        })

    return results


 


@router.get("/team-heatmap")
def get_team_heatmap(manager_id: int, days: int = 7, db: Session = Depends(get_db)):

    # 1️⃣ Get team members
    team = db.query(User).filter(User.manager_id == manager_id).all()

     # instead of today()
    latest_record = db.query(WellnessRecord)\
    .order_by(WellnessRecord.date.desc())\
    .first()

    end_date = latest_record.date if latest_record else date.today()
    start_date = end_date - timedelta(days=days)

    heatmap = defaultdict(dict)

    for emp in team:
        records = db.query(WellnessRecord).filter(
            WellnessRecord.employee_id == emp.id,
            WellnessRecord.date >= start_date,
            WellnessRecord.date <= end_date
        ).all()

        # group by date
        date_map = defaultdict(list)
        for r in records:
            date_map[r.date].append(r)

        for d in (start_date + timedelta(n) for n in range(days + 1)):

            daily_records = date_map.get(d, [])

            if not daily_records:
                heatmap[emp.id][str(d)] = "NO_DATA"
                continue

            burnout = calculate_burnout(daily_records)

            if not burnout:
                heatmap[emp.id][str(d)] = "NO_DATA"
                continue

            _, risk = burnout
            heatmap[emp.id][str(d)] = risk

    return heatmap



 