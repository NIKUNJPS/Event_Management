# Evently — Full-Stack Event Booking System

HTML + CSS + Vanilla JavaScript frontend, FastAPI backend, MySQL database.

## 1. Create database
```sql
CREATE DATABASE event_booking CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 2. Backend setup
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
pip install -r requirements.txt
copy .env.example .env   # Windows
# or cp .env.example .env
```
Edit `.env` with your MySQL username/password.

Run seed data:
```bash
python seed.py
```
Start API:
```bash
uvicorn app.main:app --reload
```
API docs: http://localhost:8000/docs

Demo admin: `admin@example.com` / `admin123`

## 3. Frontend
Serve the frontend instead of opening HTML with `file://`:
```bash
cd frontend
python -m http.server 5500
```
Open http://localhost:5500

## 4. Deploy to Render
Render has managed PostgreSQL (not MySQL); the app supports both via `DATABASE_URL`.

1. Push this folder to a GitHub repo.
2. Render Dashboard → **New → Blueprint** → select the repo. `render.yaml` creates the
   Postgres database, the `evently-api` backend and the `evently` static frontend.
3. If Render assigns different URLs than `evently-api.onrender.com` / `evently.onrender.com`,
   update `frontend/js/api.js` and the `CORS_ORIGINS` env var to match.
4. Seed from your machine using the database's **External Database URL** (PowerShell):
   ```powershell
   cd backend; $env:DATABASE_URL="<external-url>"; python seed.py
   ```
5. Log in as the seed admin and change its password immediately.

## 5. Deploy to AWS (Lambda + Amplify + RDS)
**Database (RDS MySQL):** create a MySQL 8 instance, database `event_booking`.
`DATABASE_URL=mysql+pymysql://<user>:<pass>@<rds-endpoint>:3306/event_booking`

**Backend (Lambda):**
1. `python backend/build_lambda.py` → produces `backend/lambda.zip`
2. Lambda → Create function → Python 3.12, x86_64 → upload the zip
3. Handler: `app.main.handler`; timeout 30s, memory 512 MB
4. Env vars: `DATABASE_URL`, `SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `CORS_ORIGINS` (your Amplify URL)
5. Configuration → Function URL → Auth `NONE`, **leave CORS off** (FastAPI handles it).
   (Or put an API Gateway HTTP API in front with the `$default` stage.)
6. Networking: put the Lambda in the RDS VPC and allow its security group on port 3306.
7. Seed: `cd backend; $env:DATABASE_URL="<url>"; python seed.py` from a machine that can reach RDS.

**Frontend (Amplify Hosting):** New app → connect the GitHub repo → `amplify.yml` is picked up.
Add env var `API_BASE` = `<function-url>/api` (no trailing slash), then redeploy.

## Notes
- The backend creates tables automatically on startup.
- Booking seat availability is validated server-side using a database transaction/row lock.
- For production, replace wildcard CORS, rotate the secret key, use migrations, and never keep the seed admin password.
