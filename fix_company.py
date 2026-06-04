from app.database import SessionLocal
from app import models

db = SessionLocal()


company = models.Company(name="WellSense Corp")
db.add(company)
db.commit()
db.refresh(company)

print("Created Company ID:", company.id)


users = db.query(models.User).all()

for u in users:
    u.company_id = company.id

db.commit()
db.close()

print("All users assigned to company successfully.")