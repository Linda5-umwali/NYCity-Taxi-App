from flask import Flask, jsonify
import mysql.connector
import os

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "data_loader",
    "password": "db_pass",
    "database": "nyc_taxi_db",
    "auth_plugin": "mysql_native_password"
}

TABLE_NAME = "taxi_trips"

app = Flask(__name__)

def connect_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database connection failed: {err}"}), 500

def get_data_from_db(query):
    conn = connect_db()
    if isinstance(conn, tuple):
        return conn

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except mysql.connector.Error as err:
        conn.close()
        return jsonify({"error": f"MySQL Query Error: {err}"}), 500

@app.route('/api/trip_summary', methods=['GET'])
def trip_summary():
    query = f"""
        SELECT
            COUNT(id) AS total_trips,
            AVG(trip_distance) AS avg_distance_km,
            AVG(fare_amount) AS avg_fare,
            SUM(CASE WHEN speed_outlier = TRUE THEN 1 ELSE 0 END) AS total_outliers
        FROM {TABLE_NAME};
    """
    
    result = get_data_from_db(query)

    if isinstance(result, tuple):
        return result

    if result:
        data = result[0]
        summary = {
            "total_trips": int(data['total_trips']) if data['total_trips'] is not None else 0,
            "avg_distance_km": round(float(data['avg_distance_km']), 2) if data['avg_distance_km'] is not None else 0.0,
            "avg_fare": round(float(data['avg_fare']), 2) if data['avg_fare'] is not None else 0.0,
            "total_outliers": int(data['total_outliers']) if data['total_outliers'] is not None else 0
        }
        return jsonify(summary)
    
    return jsonify({"error": "No data found"}), 404

@app.route('/api/hourly_metrics', methods=['GET'])
def hourly_metrics():
    query = f"""
        SELECT
            pickup_hour,
            COUNT(id) AS total_trips,
            AVG(trip_speed) AS avg_speed_kmh,
            AVG(fare_amount) AS avg_fare
        FROM {TABLE_NAME}
        GROUP BY pickup_hour
        ORDER BY pickup_hour;
    """
    
    result = get_data_from_db(query)

    if isinstance(result, tuple):
        return result
    
    metrics = []
    for row in result:
        metrics.append({
            "hour": row['pickup_hour'],
            "trips": int(row['total_trips']),
            "avg_speed": round(float(row['avg_speed_kmh']), 2),
            "avg_fare": round(float(row['avg_fare']), 2)
        })

    return jsonify(metrics)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
