import mysql.connector
import pandas as pd
import os

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "Linda5-umwali",
    "password": "passcode.",
    "database": "nyc_taxi_db"
}

TABLE_NAME = "taxi_trips"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(SCRIPT_DIR, "../data/cleaned/cleaned_taxi.csv")

def connect_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("Connected to MySQL.")
        return conn
    except mysql.connector.Error as err:
        print("Database connection error:", err)
        exit(1)

def create_table(cursor):
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            pickup_datetime DATETIME,
            trip_distance FLOAT,
            trip_duration_sec INT,
            passenger_count TINYINT,
            fare_amount FLOAT,
            trip_speed FLOAT,
            fare_per_km FLOAT,
            pickup_hour TINYINT,
            speed_outlier BOOLEAN
        );
    """)
    print(f"Table `{TABLE_NAME}` is ready.")

def insert_data(df, conn):
    cursor = conn.cursor()

    COLUMNS = [
        'pickup_datetime', 'trip_distance', 'trip_duration_sec', 'passenger_count',
        'fare_amount', 'trip_speed', 'fare_per_km', 'pickup_hour', 'speed_outlier'
    ]

    missing_cols = [col for col in COLUMNS if col not in df.columns]
    if missing_cols:
        print(f"Error: Missing columns in CSV chunk: {missing_cols}")
        return

    rows = df[COLUMNS].values.tolist()

    placeholders = ', '.join(['%s'] * len(COLUMNS))
    
    insert_query = f"""
        INSERT INTO {TABLE_NAME}
        ({', '.join(COLUMNS)})
        VALUES ({placeholders})
    """

    cursor.executemany(insert_query, rows)
    conn.commit()
    print(f"Inserted {cursor.rowcount} rows into `{TABLE_NAME}`.")
    cursor.close() 

def main():
    print("Loading cleaned CSV into MySQL...")
    
    CHUNKSIZE = 50000 
    total_inserted_rows = 0

    try:
        conn = connect_db()
        cursor = conn.cursor()
        create_table(cursor)
        cursor.close()

        for chunk in pd.read_csv(CSV_PATH, chunksize=CHUNKSIZE):
            chunk = chunk.where(pd.notnull(chunk), None)
            
            if 'pickup_datetime' in chunk.columns:
                 chunk['pickup_datetime'] = pd.to_datetime(chunk['pickup_datetime'])
            
            insert_data(chunk, conn)
            total_inserted_rows += len(chunk)
            print(f"  > Inserted batch. Total rows: {total_inserted_rows}")

        conn.close()
        print(f"\nSuccessfully loaded {total_inserted_rows} total rows.")
        print("Done. Connection closed.")

    except FileNotFoundError:
        print(f"\nFATAL ERROR: CSV file not found at: {CSV_PATH}")
        print("Please ensure your 'cleaned_taxi.csv' file is in the 'data/cleaned/' directory.")
        exit(1)
    except mysql.connector.Error as err:
        print(f"\nMySQL Error during data insertion: {err}")
        exit(1)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
