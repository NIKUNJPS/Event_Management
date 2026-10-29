from sqlalchemy import Column, Integer, String, Text, Date, Time, Numeric, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="user", nullable=False)
    bookings = relationship("Booking", back_populates="user")

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(80), nullable=False)
    venue = Column(String(200), nullable=False)
    event_date = Column(Date, nullable=False)
    event_time = Column(Time, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    total_seats = Column(Integer, nullable=False)
    image_url = Column(String(500), nullable=True)
    seats = relationship("Seat", back_populates="event", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="event")

class Seat(Base):
    __tablename__ = "seats"
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    seat_number = Column(String(20), nullable=False)
    is_booked = Column(Boolean, default=False, nullable=False)
    event = relationship("Event", back_populates="seats")
    booking_seats = relationship("BookingSeat", back_populates="seat")

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    booking_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(30), default="confirmed", nullable=False)
    user = relationship("User", back_populates="bookings")
    event = relationship("Event", back_populates="bookings")
    booking_seats = relationship("BookingSeat", back_populates="booking", cascade="all, delete-orphan")

class BookingSeat(Base):
    __tablename__ = "booking_seats"
    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.id"), nullable=False)
    booking = relationship("Booking", back_populates="booking_seats")
    seat = relationship("Seat", back_populates="booking_seats")
