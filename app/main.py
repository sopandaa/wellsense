 
from fastapi import FastAPI
from .database import engine
from . import models
from app.routes.auth import router as auth_router
from app.routes.wellness import router as wellness_router

app = FastAPI(title="WellSense AI")

app.include_router(auth_router)
app.include_router(wellness_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to WellSense AI Backend"}

@app.get("/health")
def health_check():
    return {"status": "System running successfully"}