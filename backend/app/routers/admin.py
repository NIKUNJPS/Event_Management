from fastapi import APIRouter, Depends
from app.database import get_db, from_dec
from app.services.auth import admin_user
router = APIRouter(prefix="/api/admin", tags=["Admin"])
@router.get("/dashboard")
def dashboard(db=Depends(get_db), _=Depends(admin_user)):
    revenue = next(db.bookings.aggregate([{"$match": {"status": "confirmed"}}, {"$group": {"_id": None, "total": {"$sum": "$total_amount"}}}]), None)
    return {"users": db.users.count_documents({}), "events": db.events.count_documents({}), "bookings": db.bookings.count_documents({}), "revenue": float(from_dec(revenue["total"])) if revenue else 0.0}
