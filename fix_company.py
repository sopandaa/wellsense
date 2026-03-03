from app.database import SessionLocal
from app import models

db = SessionLocal()

# 1️⃣ Create company
company = models.Company(name="WellSense Corp")
db.add(company)
db.commit()
db.refresh(company)

print("Created Company ID:", company.id)

# 2️⃣ Assign all users to this company
users = db.query(models.User).all()

for u in users:
    u.company_id = company.id

db.commit()
db.close()

print("All users assigned to company successfully.")