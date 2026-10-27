from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os

app = FastAPI()

# Allows GitHub Pages URL to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://rkomtchuente.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# connects to database
def get_db_connection():
    return psycopg2.connect(os.environ["DB_URL"])

@app.get("/api/events")
def get_events():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT event_id, title, category, event_date, latitude, longitude FROM Events;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    events = []
    for row in rows:
        events.append({
            "id": row[0],
            "title": row[1],
            "category": row[2],
            "date": row[3],
            "lat": row[4],
            "lon": row[5]
        })
    return {"events": events}