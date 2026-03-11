from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.routes.auth import get_current_user
from app import models
from app.services.burnout_service import calculate_burnout
from sqlalchemy import desc

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