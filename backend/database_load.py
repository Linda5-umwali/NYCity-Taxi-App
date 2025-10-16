import mysql.connector
import pandas as pd
import os

# --- CONFIG ---
DB_CONFIG = {
    "host": "localhost",
    "user": "Linda5-umwali",
    "password": "passcode.",
    "database": "nyc_taxi_db"
}

TABLE_NAME = "taxi_trips"
CSV_PATH = "../data/cleaned/cleaned_taxi.csv"

# --- CONNECT TO DATABASE ---
def connect_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("Connected to MySQL.")
        return conn
    except mysql.connector.Error as err:
        print("Database connection error:", err)
        exit(1)

# --- CREATE TABLE IF NOT EXISTS ---
def create_table(cursor):
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            pickup_datetime DATETIME,
            trip_distance FLOAT,
            trip_duration_sec INT,
            passenger_count INT,
            fare_amount FLOAT,
            trip_speed FLOAT,
            fare_per_km FLOAT,
            pickup_hour INT,
            speed_outlier BOOLEAN
        );
    """)
    print(f"Table `{TABLE_NAME}` is ready.")

# --- INSERT DATA ---
def insert_data(df, conn):
    cursor = conn.cursor()
    create_table(cursor)

    insert_query = f"""
        INSERT INTO {TABLE_NAME} 
        (pickup_datetime, trip_distance, trip_duration_sec, passenger_count,
         fare_amount, trip_speed, fare_per_km, pickup_hour, speed_outlier)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    rows = df[[
        'pickup_datetime', 'trip_distance', 'trip_duration_sec', 'passenger_count',
        'fare_amount', 'trip_speed', 'fare_per_km', 'pickup_hour', 'speed_outlier'
    ]].values.tolist()

    cursor.executemany(insert_query, rows)
    conn.commit()
    print(f"Inserted {cursor.rowcount} rows into `{TABLE_NAME}`.")

# --- MAIN ---
def main():
    print("Loading cleaned CSV into MySQL...")
    df = pd.read_csv(CSV_PATH)

    conn = connect_db()
    insert_data(df, conn)

    conn.close()
    print("Done. Connection closed.")

if __name__ == "__main__":
    main()
