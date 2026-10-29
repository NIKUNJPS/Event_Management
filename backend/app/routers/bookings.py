from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.models import Event, Seat, Booking, BookingSeat
from app.schemas import BookingCreate, BookingOut
from app.services.auth import current_user
router = APIRouter(prefix="/api/bookings", tags=["Bookings"])

def serialize(b):
    return {"id": b.id, "event_id": b.event_id, "total_amount": b.total_amount, "status": b.status,
            "seat_numbers": [x.seat.seat_number for x in b.booking_seats], "event_title": b.event.title}

@router.post("", response_model=BookingOut)
def create_booking(data: BookingCreate, db: Session = Depends(get_db), user=Depends(current_user)):
    event = db.get(Event, data.event_id)
    if not event: raise HTTPException(404, "Event not found")
    if len(set(data.seat_ids)) != len(data.seat_ids): raise HTTPException(400, "Duplicate seats selected")
    seats = db.execute(select(Seat).where(Seat.id.in_(data.seat_ids), Seat.event_id == event.id).with_for_update()).scalars().all()
    if len(seats) != len(data.seat_ids): raise HTTPException(400, "Invalid seat selection")
    if any(s.is_booked for s in seats): raise HTTPException(409, "One or more seats are already booked")
    booking = Booking(user_id=user.id, event_id=event.id, total_amount=event.price * len(seats))
    db.add(booking); db.flush()
    for seat in seats:
        seat.is_booked = True; db.add(BookingSeat(booking_id=booking.id, seat_id=seat.id))
    db.commit(); db.refresh(booking); return serialize(booking)

@router.get("/my", response_model=list[BookingOut])
def my_bookings(db: Session = Depends(get_db), user=Depends(current_user)):
    return [serialize(b) for b in db.query(Booking).filter(Booking.user_id == user.id).order_by(Booking.booking_date.desc()).all()]

@router.delete("/{booking_id}")
def cancel_booking(booking_id: int, db: Session = Depends(get_db), user=Depends(current_user)):
    booking = db.get(Booking, booking_id)
    if not booking or booking.user_id != user.id: raise HTTPException(404, "Booking not found")
    if booking.status == "cancelled": raise HTTPException(400, "Booking already cancelled")
    for bs in booking.booking_seats: bs.seat.is_booked = False
    booking.status = "cancelled"; db.commit(); return {"message": "Booking cancelled"}
