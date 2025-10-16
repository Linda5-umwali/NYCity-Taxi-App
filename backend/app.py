from flask import Flask, jsonify, request
import pandas as pd
import os

CLEANED_DATA_PATH = "../data/cleaned/cleaned_taxi.csv"

app = Flask(__name__)

# Load cleaned data into memory once at startup
if not os.path.exists(CLEANED_DATA_PATH):
    raise FileNotFoundError(f"Cleaned CSV not found at {CLEANED_DATA_PATH}. Run data_processing.py first.")

df = pd.read_csv(CLEANED_DATA_PATH)

def filter_trips(dataframe, params):
    """Filter trips based on query parameters"""
    df_filtered = dataframe.copy()

    # Filter by pickup_hour
    if "pickup_hour" in params:
        hours = [int(h) for h in params.get("pickup_hour").split(",")]
        df_filtered = df_filtered[df_filtered['pickup_hour'].isin(hours)]

    # Filter by trip_distance
    min_dist = float(params.get("min_distance", 0))
    max_dist = float(params.get("max_distance", df_filtered['trip_distance'].max()))
    df_filtered = df_filtered[(df_filtered['trip_distance'] >= min_dist) & (df_filtered['trip_distance'] <= max_dist)]

    # Filter by trip_speed
    max_speed = float(params.get("max_speed", df_filtered['trip_speed'].max()))
    df_filtered = df_filtered[df_filtered['trip_speed'] <= max_speed]

    return df_filtered

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to NYC Taxi API!",
        "endpoints": ["/trips", "/stats/peak-hours", "/stats/speed-outliers"]
    })

@app.route("/trips", methods=["GET"])
def get_trips():
    """Return trips, optionally filtered by query parameters"""
    filtered_df = filter_trips(df, request.args)
    # Return only first 100 rows for performance
    return jsonify(filtered_df.head(100).to_dict(orient="records"))

@app.route("/stats/peak-hours", methods=["GET"])
def get_peak_hours():
    """Return peak hours based on trip volume"""
    hourly_counts = df['pickup_hour'].value_counts().sort_index()
    mean_count = hourly_counts.mean()
    std_count = hourly_counts.std()
    peak_hours = hourly_counts[hourly_counts > (mean_count + std_count)].index.tolist()
    return jsonify({"peak_hours": peak_hours})

@app.route("/stats/speed-outliers", methods=["GET"])
def get_speed_outliers():
    """Return trips flagged as speed outliers"""
    outliers = df[df['speed_outlier'] == True]
    return jsonify(outliers.head(100).to_dict(orient="records"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
