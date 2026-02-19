from fastapi import FastAPI

app = FastAPI(title="WellSense AI")

@app.get("/")
def read_root():
    return {"message": "Welome to WellSense AI Backend"}

@app.get("/health")

def health_check():
    return {"status": "System running successfully"}