from fastapi import FastAPI, Form, Depends
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="UWA Backend")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "UWA API is running"}

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

from fastapi.middleware.cors import CORSMiddleware

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------- ADMIN ENDPOINTS --------

@app.get("/admin/tourists")
def get_tourists(db: Session = Depends(get_db)):
    return db.query(models.Tourist).all()

@app.get("/admin/transit")
def get_transit(db: Session = Depends(get_db)):
    return db.query(models.Transit).all()

@app.get("/admin/students")
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()


from datetime import date
from sqlalchemy import func

@app.get("/admin/daily-summary")
def daily_summary(db: Session = Depends(get_db)):
    today = date.today()

    tourists = db.query(func.count(models.Tourist.id))\
        .filter(func.date(models.Tourist.created_at) == today).scalar()

    transit = db.query(func.count(models.Transit.id))\
        .filter(func.date(models.Transit.created_at) == today).scalar()

    students = db.query(func.count(models.Student.id))\
        .filter(func.date(models.Student.created_at) == today).scalar()

    return {
        "date": str(today),
        "tourists": tourists,
        "transit": transit,
        "students": students,
        "total_visitors": tourists + transit + students
    }

from fastapi.responses import FileResponse
import openpyxl

@app.get("/admin/export/tourists")
def export_tourists(db: Session = Depends(get_db)):
    tourists = db.query(models.Tourist).all()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Tourists"

    ws.append(["Name", "Contact", "Visitor Type", "Nationality", "Date"])

    for t in tourists:
        ws.append([
            t.name,
            t.contact,
            t.visitor_type,
            t.nationality,
            t.created_at.strftime("%Y-%m-%d %H:%M")
        ])

    file_path = "tourists_report.xlsx"
    wb.save(file_path)

    return FileResponse(
        file_path,
        filename="tourists_report.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

from fastapi import HTTPException

ADMIN_USER = "admin"
ADMIN_PASS = "uwa123"

@app.post("/admin/login")
def admin_login(username: str = Form(...), password: str = Form(...)):
    if username == ADMIN_USER and password == ADMIN_PASS:
        return {"status": "success"}
    raise HTTPException(status_code=401, detail="Invalid credentials")



