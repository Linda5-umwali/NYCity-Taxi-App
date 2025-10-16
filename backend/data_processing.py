"""
NYC Taxi Data Processing Script
Cleans raw data, creates derived features, detects outliers,
and prepares data for backend API use.
"""

import pandas as pd
import numpy as np
import os

# Paths
RAW_DATA_PATH = "../data/raw/train.csv"
CLEANED_DATA_PATH = "../data/cleaned/cleaned_taxi.csv"
LOG_PATH = "../data/logs/cleaning_log.txt"

def calculate_haversine_distance(df):
    R = 6371
    #convert degrees to radians
    lon1 = np.radians(df['pickup_longitude'])
    lat1 = np.radians(df['pickup_latitude'])
    lon2 = np.radians(df['dropoff_longitude'])
    lat2 = np.radians(df['dropoff_latitude'])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon /2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

    distance = R * c
    return distance

def estimate_trip_fare(distance_km, duration_sec, passenger_count=1):
    """
    Estimate a trip fare based on distance, duration, and passenger count.
    """
    duration_min = duration_sec / 60
    base_fare = 2.50
    distance_fare = distance_km * 1.50
    time_fare = duration_min * 0.35
    passenger_surcharge = max(0, passenger_count - 1) * 0.50
    total_fare = max(3.50, base_fare + distance_fare + time_fare)
    return round(total_fare + passenger_surcharge, 2)

def identify_peak_hours(df):
    """
    Identify peak hours based on trip volume.
    Returns a list of hour integers (0-23)
    """
    hourly_counts = df['pickup_hour'].value_counts().sort_index()
    peak_hours = hourly_counts.nlargest(2).index.tolist()
    return peak_hours

def detect_speed_outliers(speeds, threshold=80):
    """
    Detect trips with speeds exceeding threshold km/h
    Returns a boolean Series
    """
    return speeds > threshold

def clean_data():
    # Load CSV
    df = pd.read_csv(RAW_DATA_PATH)
    df.rename(columns={'trip_duration': 'trip_duration_sec'}, inplace=True)
    df['trip_distance'] = calculate_haversine_distance(df)

    #estimated fare amount
    df['fare_amount'] = df.apply(
        lambda row: estimate_trip_fare(row['trip_distance'], row['trip_duration_sec'], row['passenger_count']),
        axis=1
            )

    # Check required columns
    required_cols = ['fare_amount', 'trip_distance', 'trip_duration_sec', 'pickup_datetime', 'passenger_count']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Remove duplicates & missing values
    initial_count = len(df)
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)
    after_clean_count = len(df)
    
    # Handle invalid records
    invalid_records = df[(df['trip_distance'] < 0.1) | (df['trip_duration_sec'] <= 60)]
    invalid_count = len(invalid_records)

    os.makedirs("../data/logs", exist_ok=True)
    with open(LOG_PATH, "w") as log:
        log.write(f"Rows before cleaning: {initial_count}\n")
        log.write(f"Rows after dropna & duplicates: {after_clean_count}\n")
        log.write(f"Removed {invalid_count} invalid records based on trip distance/duration\n")
    df = df[(df['trip_distance'] >= 0.1) & (df['trip_duration_sec'] > 60)]

    # Derived features
    df['trip_speed'] = df['trip_distance'] / (df['trip_duration_sec'] / 3600)  # km/h
    df['fare_per_km'] = df['fare_amount'] / df['trip_distance']
    df['pickup_hour'] = pd.to_datetime(df['pickup_datetime']).dt.hour

    # Custom algorithm: flag speed outliers
    df['speed_outlier'] = detect_speed_outliers(df['trip_speed'])

    # Peak hours
    peak_hours = identify_peak_hours(df)
    print("Identified peak hours (Top 2):", peak_hours)

    # Save cleaned CSV
    os.makedirs("../data/cleaned", exist_ok=True)
    df.to_csv(CLEANED_DATA_PATH, index=False)
    print(f"Data cleaned and saved to {CLEANED_DATA_PATH}")
    print("Sample rows:\n", df[['pickup_datetime', 'trip_distance', 'trip_duration_sec', 'fare_amount', 'trip_speed']].head())

if __name__ == "__main__":
    clean_data()
