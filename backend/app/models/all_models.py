# MongoDB collections (documents use integer _id from the `counters` collection):
#   users     {_id, name, email, password_hash, role}
#   events    {_id, title, description, category, venue, event_date "YYYY-MM-DD",
#              event_time "HH:MM:SS", price Decimal128, total_seats, image_url}
#   seats     {_id, event_id, seat_number, is_booked}
#   bookings  {_id, user_id, event_id, event_title, seat_ids, seat_numbers,
#              booking_date, total_amount Decimal128, status}
from app.database import from_dec

def event_out(doc):
    return {"id": doc["_id"], "title": doc["title"], "description": doc["description"], "category": doc["category"],
            "venue": doc["venue"], "event_date": doc["event_date"], "event_time": doc["event_time"],
            "price": from_dec(doc["price"]), "total_seats": doc["total_seats"], "image_url": doc.get("image_url")}

def booking_out(doc):
    return {"id": doc["_id"], "event_id": doc["event_id"], "total_amount": from_dec(doc["total_amount"]), "status": doc["status"],
            "seat_numbers": doc["seat_numbers"], "event_title": doc["event_title"]}

def seat_label(i, cols): return f"{chr(65 + i // cols)}{i % cols + 1}"
