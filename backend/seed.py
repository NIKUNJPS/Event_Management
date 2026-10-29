from datetime import date, timedelta
from app.database import db, init_db, next_id, next_ids, dec128
from app.models import seat_label
from app.services.auth import hash_password

init_db()
if not db.users.find_one({'email': 'admin@example.com'}):
    db.users.insert_one({'_id': next_id(db, 'users'), 'name': 'Admin', 'email': 'admin@example.com', 'password_hash': hash_password('admin123'), 'role': 'admin'})
if db.events.count_documents({}) == 0:
    samples=[('Indie Music Night','Live music and local artists.','Music','Pune Arena',499),('Tech Connect 2026','A practical technology conference.','Technology','Convention Hall, Pune',799),('Stand-up Comedy Night','An evening of live comedy.','Comedy','City Theatre, Pune',399)]
    for i,(t,d,c,v,p) in enumerate(samples):
        eid = next_id(db, 'events')
        db.events.insert_one({'_id': eid, 'title': t, 'description': d, 'category': c, 'venue': v, 'event_date': (date.today()+timedelta(days=10+i*7)).isoformat(), 'event_time': '19:00:00', 'price': dec128(p), 'total_seats': 40, 'image_url': ''})
        db.seats.insert_many([{'_id': sid, 'event_id': eid, 'seat_number': seat_label(n, 10), 'is_booked': False} for n, sid in enumerate(next_ids(db, 'seats', 40))])
print('Seed complete. Admin: admin@example.com / admin123')
