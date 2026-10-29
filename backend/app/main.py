import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from app.database import init_db
from app.routers import auth, events, bookings, admin

init_db()
app = FastAPI(title="Event Booking API", version="1.0.0")
# Comma-separated list, e.g. https://evently.onrender.com; defaults to * for local dev
origins = [o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",") if o.strip()]
# Optional regex for hosts with generated suffixes, e.g. https://evently(-[a-z0-9]+)?\.onrender\.com
origin_regex = os.getenv("CORS_ORIGIN_REGEX") or None
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_origin_regex=origin_regex, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(auth.router); app.include_router(events.router); app.include_router(bookings.router); app.include_router(admin.router)
@app.get("/")
def root(): return {"message": "Event Booking API is running"}

# AWS Lambda entry point (handler: app.main.handler); uvicorn ignores it
handler = Mangum(app, lifespan="off")
