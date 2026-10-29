from datetime import date, time
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class RegisterIn(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class EventCreate(BaseModel):
    title: str
    description: str
    category: str
    venue: str
    event_date: date
    event_time: time
    price: Decimal
    total_seats: int = Field(gt=0, le=10000)
    image_url: str | None = None

class EventOut(EventCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class BookingCreate(BaseModel):
    event_id: int
    seat_ids: list[int] = Field(min_length=1)

class BookingOut(BaseModel):
    id: int
    event_id: int
    total_amount: Decimal
    status: str
    seat_numbers: list[str]
    event_title: str
    model_config = ConfigDict(from_attributes=True)
