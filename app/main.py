from fastapi import FastAPI
from .database import engine
from . import models
from .routes import auth
 


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="WellSense AI")
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"message": "Welome to WellSense AI Backend"}

@app.get("/health")

def health_check():
    return {"status": "System running successfully"}


