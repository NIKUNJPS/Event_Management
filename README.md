# Evently — Full-Stack Event Booking System

HTML + CSS + Vanilla JavaScript frontend, FastAPI backend, MongoDB database.

## 1. Create database
Create a free cluster on MongoDB Atlas (or run MongoDB locally). Collections and indexes
are created automatically; no schema setup is needed.

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
Set `MONGODB_URL` in `.env` to your connection string (the database name in the URL is used, default `event_booking`).

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
1. Push this folder to a GitHub repo.
2. Render Dashboard → **New → Blueprint** → select the repo. `render.yaml` creates the
   `evently-api` backend and the `evently` static frontend.
3. In `evently-api` → **Environment**, set `MONGODB_URL` to your Atlas connection string.
   In Atlas → **Network Access**, allow `0.0.0.0/0` (Render free instances have no fixed IP).
4. If Render assigns a different backend URL, update `frontend/js/api.js`.
5. Seed from your machine (PowerShell):
   ```powershell
   cd backend; $env:MONGODB_URL="<atlas-url>"; python seed.py
   ```
6. Log in as the seed admin and change its password immediately.

## 5. Deploy to AWS (Lambda + Amplify)
**Database:** use the same MongoDB Atlas cluster (`MONGODB_URL`).

**Backend (Lambda):**
1. `python backend/build_lambda.py` → produces `backend/lambda.zip`
2. Lambda → Create function → Python 3.12, x86_64 → upload the zip
3. Handler: `app.main.handler`; timeout 30s, memory 512 MB
4. Env vars: `MONGODB_URL`, `SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `CORS_ORIGINS` (your Amplify URL)
5. Configuration → Function URL → Auth `NONE`, **leave CORS off** (FastAPI handles it).
   (Or put an API Gateway HTTP API in front with the `$default` stage.)
6. Networking: allow Lambda's outbound IPs in Atlas Network Access (or `0.0.0.0/0`).
7. Seed: `cd backend; $env:MONGODB_URL="<url>"; python seed.py`.

**Frontend (Amplify Hosting):** New app → connect the GitHub repo → `amplify.yml` is picked up.
Add env var `API_BASE` = `<function-url>/api` (no trailing slash), then redeploy.

## Notes
- The backend creates MongoDB indexes automatically on startup.
- Booking seat availability is validated server-side by claiming each seat with a conditional update (never double-booked).
- For production, replace wildcard CORS, rotate the secret key, use migrations, and never keep the seed admin password.
