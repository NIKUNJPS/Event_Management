from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db, next_id, to_dec, dec128, from_dec
from app.models import booking_out
from app.schemas import BookingCreate, BookingOut
from app.services.auth import current_user
router = APIRouter(prefix="/api/bookings", tags=["Bookings"])

@router.post("", response_model=BookingOut)
def create_booking(data: BookingCreate, db=Depends(get_db), user=Depends(current_user)):
    event = db.events.find_one({"_id": data.event_id})
    if not event: raise HTTPException(404, "Event not found")
    if len(set(data.seat_ids)) != len(data.seat_ids): raise HTTPException(400, "Duplicate seats selected")
    seats = list(db.seats.find({"_id": {"$in": data.seat_ids}, "event_id": event["_id"]}))
    if len(seats) != len(data.seat_ids): raise HTTPException(400, "Invalid seat selection")
    # Claim each seat with a conditional update so two users can never book the same seat;
    # if any claim fails, release the seats this request already claimed.
    claimed = []
    for seat in seats:
        if db.seats.update_one({"_id": seat["_id"], "is_booked": False}, {"$set": {"is_booked": True}}).modified_count != 1:
            if claimed: db.seats.update_many({"_id": {"$in": claimed}}, {"$set": {"is_booked": False}})
            raise HTTPException(409, "One or more seats are already booked")
        claimed.append(seat["_id"])
    booking = {"_id": next_id(db, "bookings"), "user_id": user["_id"], "event_id": event["_id"], "event_title": event["title"],
               "seat_ids": claimed, "seat_numbers": [s["seat_number"] for s in seats], "booking_date": datetime.now(timezone.utc),
               "total_amount": dec128(to_dec(from_dec(event["price"])) * len(seats)), "status": "confirmed"}
    db.bookings.insert_one(booking); return booking_out(booking)

@router.get("/my", response_model=list[BookingOut])
def my_bookings(db=Depends(get_db), user=Depends(current_user)):
    return [booking_out(b) for b in db.bookings.find({"user_id": user["_id"]}).sort("booking_date", -1)]

@router.delete("/{booking_id}")
def cancel_booking(booking_id: int, db=Depends(get_db), user=Depends(current_user)):
    booking = db.bookings.find_one({"_id": booking_id, "user_id": user["_id"]})
    if not booking: raise HTTPException(404, "Booking not found")
    if booking["status"] == "cancelled": raise HTTPException(400, "Booking already cancelled")
    db.seats.update_many({"_id": {"$in": booking["seat_ids"]}}, {"$set": {"is_booked": False}})
    db.bookings.update_one({"_id": booking_id}, {"$set": {"status": "cancelled"}}); return {"message": "Booking cancelled"}
