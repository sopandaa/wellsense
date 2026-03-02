from datetime import date, timedelta
import random
from app.database import SessionLocal
from app import models

db = SessionLocal()

# Get all employees
employees = db.query(models.User).filter(models.User.role == "EMPLOYEE").all()

for employee in employees:
    base_fatigue = random.randint(3, 6)
    base_stress = random.randint(3, 6)
    base_sleep = random.uniform(6, 8)
    base_productivity = random.randint(6, 8)

    for i in range(14):
        record_date = date.today() - timedelta(days=i)

        record = models.WellnessRecord(
            employee_id=employee.id,
            date=record_date,
            work_hours=random.uniform(6, 9),
            fatigue_score=min(10, max(1, int(base_fatigue + random.uniform(-1, 2)))),
            stress_level=min(10, max(1, int(base_stress + random.uniform(-1, 2)))),
            sleep_hours=max(3, base_sleep + random.uniform(-1, 1)),
            productivity_score=min(10, max(1, int(base_productivity + random.uniform(-2, 1))))
        )

        db.add(record)

db.commit()
db.close()

print("14 days of wellness data seeded successfully.")