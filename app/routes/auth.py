from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from app.utils.security import hash_password
from fastapi import HTTPException
from app.utils.security import verify_password, create_access_token
from sqlalchemy.orm import Session
from app import models
from app.database import get_db
from fastapi import Depends
from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.security import verify_token
from fastapi import status
router = APIRouter()

@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Check if email already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role=user.role,
        department=user.department
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    
     
    
    access_token = create_access_token(
    data={
        "sub": user.email,
        "user_id": user.id,
        "role": user.role,
        "company_id": user.company_id
    }
    )   
    
     
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    } 

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    email = verify_token(token)

    if email is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(models.User).filter(models.User.email == email).first()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user



def require_admin(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Admins only"
        )
    return current_user

@router.get("/protected")
def protected_route(current_user: models.User = Depends(get_current_user)):
    return {
        "message": f"Hello {current_user.name}, you are authenticated!",
        "email": current_user.email,
        "role": current_user.role,
        "department": current_user.department
    }

@router.get("/admin/dashboard")
def admin_dashboard(admin_user: models.User = Depends(require_admin)):
    return {
        "message": f"Welcome Admin {admin_user.name}",
        "email": admin_user.email,
        "role": admin_user.role
    }


@router.get("/test-auth")
def test_auth(current_user: models.User = Depends(get_current_user)):
    return {
        "email": current_user.email,
        "role": current_user.role
    }



@router.get("/admin-test")
def admin_test(current_user: models.User = Depends(require_admin)):
    return {"message": "Welcome Admin"}



@router.get("/users")
def get_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.User).filter(
        models.User.company_id == current_user.company_id
    ).all()


@router.get("/company-users")
def company_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):
    return db.query(models.User).filter(
        models.User.company_id == current_user.company_id
    ).all()