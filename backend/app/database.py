import os
from decimal import Decimal
from bson import Decimal128
from dotenv import load_dotenv
from pymongo import MongoClient, ReturnDocument, ASCENDING, DESCENDING

load_dotenv()
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/event_booking")
client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=10000)
# Uses the database named in the URL, else event_booking
db = client.get_default_database(default="event_booking")

def init_db(database=db):
    database.users.create_index("email", unique=True)
    database.seats.create_index([("event_id", ASCENDING), ("_id", ASCENDING)])
    database.bookings.create_index([("user_id", ASCENDING), ("booking_date", DESCENDING)])

def next_ids(database, name, count=1):
    """Reserve `count` sequential integer ids; the frontend relies on numeric ids."""
    doc = database.counters.find_one_and_update({"_id": name}, {"$inc": {"seq": count}}, upsert=True, return_document=ReturnDocument.AFTER)
    return list(range(doc["seq"] - count + 1, doc["seq"] + 1))

def next_id(database, name): return next_ids(database, name)[0]

def to_dec(value): return Decimal(str(value))
def dec128(value): return Decimal128(str(value))
def from_dec(value): return (value.to_decimal() if isinstance(value, Decimal128) else Decimal(str(value))).quantize(Decimal("0.01"))

def get_db():
    return db
