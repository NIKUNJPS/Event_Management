from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db, next_id, next_ids, dec128
from app.models import event_out, seat_label
from app.schemas import EventCreate, EventOut
from app.services.auth import admin_user
router = APIRouter(prefix="/api/events", tags=["Events"])

@router.get("", response_model=list[EventOut])
def list_events(db=Depends(get_db)):
    return [event_out(e) for e in db.events.find().sort([("event_date", 1), ("event_time", 1)])]

@router.get("/{event_id}", response_model=EventOut)
def get_event(event_id: int, db=Depends(get_db)):
    event = db.events.find_one({"_id": event_id})
    if not event: raise HTTPException(404, "Event not found")
    return event_out(event)

@router.get("/{event_id}/seats")
def seats(event_id: int, db=Depends(get_db)):
    if not db.events.find_one({"_id": event_id}, {"_id": 1}): raise HTTPException(404, "Event not found")
    return [{"id": s["_id"], "seat_number": s["seat_number"], "is_booked": s["is_booked"]} for s in db.seats.find({"event_id": event_id}).sort("_id", 1)]

@router.post("", response_model=EventOut)
def create_event(data: EventCreate, db=Depends(get_db), _=Depends(admin_user)):
    event = {"_id": next_id(db, "events"), **data.model_dump(), "event_date": data.event_date.isoformat(),
             "event_time": data.event_time.isoformat(), "price": dec128(data.price)}
    db.events.insert_one(event)
    cols = min(10, data.total_seats)
    ids = next_ids(db, "seats", data.total_seats)
    db.seats.insert_many([{"_id": sid, "event_id": event["_id"], "seat_number": seat_label(i, cols), "is_booked": False} for i, sid in enumerate(ids)])
    return event_out(event)

@router.delete("/{event_id}")
def delete_event(event_id: int, db=Depends(get_db), _=Depends(admin_user)):
    if not db.events.find_one_and_delete({"_id": event_id}): raise HTTPException(404, "Event not found")
    db.seats.delete_many({"event_id": event_id}); return {"message": "Event deleted"}
