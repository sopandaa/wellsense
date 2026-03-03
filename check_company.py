from app.database import SessionLocal
from app import models

db = SessionLocal()

users = db.query(models.User).all()
for u in users:
    print(u.id, u.role, u.company_id, u.department)