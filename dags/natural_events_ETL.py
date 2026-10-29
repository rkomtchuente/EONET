import os
import requests
import psycopg2
from dotenv import load_dotenv

def eonet_etl():
    # gets variables from the .env file
    load_dotenv()
    api_key = os.environ["EONET_API_KEY"]
    dbpwd = os.environ["PGPASSWORD"]

    # gets live open events data from EONET
    url = f"https://eonet.gsfc.nasa.gov/api/v3/events?status=open&days=20&api_key={api_key}"
    response = requests.get(url)

    # Handle potential API errors before processing
    response.raise_for_status() 
    events = response.json().get('events', [])

    # Connect to database
    conn = psycopg2.connect(host="postgres-hnn6", port=5432, dbname='EONET', user='postgres', password=dbpwd)
    cur = conn.cursor()

    # creates table if does not exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Events (
            event_id VARCHAR(100) PRIMARY KEY,
            title TEXT,
            category TEXT,
            event_date TIMESTAMP,
            latitude FLOAT,
            longitude FLOAT
        );
    """)

    # the following lines of code Parses the Json file and Upsert data to our database
    for event in events:
        event_id = event['id']
        title = event['title']
        category = event['categories'][0]['title']
        
        if event.get('geometry'):
            latest_geo = event['geometry'][-1] 
            date = latest_geo['date']
            lon, lat = latest_geo['coordinates'][0], latest_geo['coordinates'][1]

            # Insert data into database. if duplicate event_id, update.
            query = """
                INSERT INTO Events (event_id, title, category, event_date, latitude, longitude)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (event_id) DO UPDATE
                SET event_date = EXCLUDED.event_date, 
                    latitude = EXCLUDED.latitude, 
                    longitude = EXCLUDED.longitude;
            """
            cur.execute(query, (event_id, title, category, date, lat, lon))

    conn.commit()
    cur.close()
    conn.close()
