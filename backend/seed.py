from datetime import date, time, timedelta
from app.database import SessionLocal
from app.models import User, Event, Seat
from app.services.auth import hash_password

db=SessionLocal()
if not db.query(User).filter(User.email=='admin@example.com').first():
    db.add(User(name='Admin', email='admin@example.com', password_hash=hash_password('admin123'), role='admin'))
if db.query(Event).count()==0:
    samples=[('Indie Music Night','Live music and local artists.','Music','Pune Arena',499),('Tech Connect 2026','A practical technology conference.','Technology','Convention Hall, Pune',799),('Stand-up Comedy Night','An evening of live comedy.','Comedy','City Theatre, Pune',399)]
    for i,(t,d,c,v,p) in enumerate(samples):
        e=Event(title=t,description=d,category=c,venue=v,event_date=date.today()+timedelta(days=10+i*7),event_time=time(19,0),price=p,total_seats=40,image_url='')
        db.add(e); db.flush()
        for n in range(40): db.add(Seat(event_id=e.id,seat_number=f'{chr(65+n//10)}{n%10+1}'))
db.commit(); db.close(); print('Seed complete. Admin: admin@example.com / admin123')
