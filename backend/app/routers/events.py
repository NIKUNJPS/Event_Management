from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Event, Seat
from app.schemas import EventCreate, EventOut
from app.services.auth import admin_user
router = APIRouter(prefix="/api/events", tags=["Events"])

@router.get("", response_model=list[EventOut])
def list_events(db: Session = Depends(get_db)):
    return db.query(Event).order_by(Event.event_date, Event.event_time).all()

@router.get("/{event_id}", response_model=EventOut)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.get(Event, event_id)
    if not event: raise HTTPException(404, "Event not found")
    return event

@router.get("/{event_id}/seats")
def seats(event_id: int, db: Session = Depends(get_db)):
    if not db.get(Event, event_id): raise HTTPException(404, "Event not found")
    return [{"id": s.id, "seat_number": s.seat_number, "is_booked": s.is_booked} for s in db.query(Seat).filter(Seat.event_id == event_id).order_by(Seat.id)]

@router.post("", response_model=EventOut)
def create_event(data: EventCreate, db: Session = Depends(get_db), _=Depends(admin_user)):
    event = Event(**data.model_dump()); db.add(event); db.flush()
    cols = min(10, event.total_seats)
    for i in range(event.total_seats): db.add(Seat(event_id=event.id, seat_number=f"{chr(65 + i // cols)}{i % cols + 1}"))
    db.commit(); db.refresh(event); return event

@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db), _=Depends(admin_user)):
    event = db.get(Event, event_id)
    if not event: raise HTTPException(404, "Event not found")
    db.delete(event); db.commit(); return {"message": "Event deleted"}
