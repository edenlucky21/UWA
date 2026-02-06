from fastapi import FastAPI, Form, Depends
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="UWA Park Entry Backend")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "UWA Park Entry API is running"}

# ---------------- TOURIST ----------------
@app.post("/tourist")
def submit_tourist(
    client_name: str = Form(...),
    client_contact: str = Form(...),
    visitor_type: str = Form(...),
    nationality: str = Form(...),
    db: Session = Depends(get_db)
):
    tourist = models.Tourist(
        name=client_name,
        contact=client_contact,
        visitor_type=visitor_type,
        nationality=nationality
    )
    db.add(tourist)
    db.commit()
    return {"status": "Tourist saved"}

# ---------------- TRANSIT ----------------
@app.post("/transit")
def submit_transit(
    transit_name: str = Form(...),
    transit_contact: str = Form(...),
    transit_reg: str = Form(...),
    visitor_type: str = Form(...),
    nationality: str = Form(...),
    db: Session = Depends(get_db)
):
    transit = models.Transit(
        name=transit_name,
        contact=transit_contact,
        vehicle_reg=transit_reg,
        visitor_type=visitor_type,
        nationality=nationality
    )
    db.add(transit)
    db.commit()
    return {"status": "Transit visitor saved"}

# ---------------- STUDENT ----------------
@app.post("/student")
def submit_student(
    student_school: str = Form(...),
    institution: str = Form(...),
    student_contact: str = Form(...),
    visitor_type: str = Form(...),
    nationality: str = Form(...),
    db: Session = Depends(get_db)
):
    student = models.Student(
        school=student_school,
        institution=institution,
        contact=student_contact,
        visitor_type=visitor_type,
        nationality=nationality
    )
    db.add(student)
    db.commit()
    return {"status": "Student saved"}