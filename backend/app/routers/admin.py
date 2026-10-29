from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import User, Event, Booking
from app.services.auth import admin_user
router = APIRouter(prefix="/api/admin", tags=["Admin"])
@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), _=Depends(admin_user)):
    return {"users": db.query(func.count(User.id)).scalar(), "events": db.query(func.count(Event.id)).scalar(), "bookings": db.query(func.count(Booking.id)).scalar(), "revenue": float(db.query(func.coalesce(func.sum(Booking.total_amount), 0)).filter(Booking.status == "confirmed").scalar() or 0)}
