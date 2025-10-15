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


def estimate_trip_fare(distance_km, duration_min, passenger_count=1):
    """
    Estimate a trip fare based on distance, duration, and passenger count.
    """
    base_fare = 2.50
    distance_fare = distance_km * 2.50
    time_fare = duration_min * 0.50
    passenger_surcharge = max(0, passenger_count - 1) * 0.50
    total_fare = base_fare + distance_fare + time_fare + passenger_surcharge
    return round(total_fare, 2)

def identify_peak_hours(df):
    """
    Identify peak hours based on trip volume.
    Returns a list of hour integers (0-23)
    """
    hourly_counts = df['pickup_hour'].value_counts().sort_index()
    mean_count = hourly_counts.mean()
    std_count = hourly_counts.std()
    peak_hours = hourly_counts[hourly_counts > (mean_count + std_count)].index.tolist()
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

    # Check required columns
    required_cols = ['fare_amount', 'trip_distance', 'trip_duration', 'pickup_datetime', 'passenger_count']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Remove duplicates & missing values
    initial_count = len(df)
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)
    after_clean_count = len(df)

    # Handle invalid records
    invalid_records = df[(df['fare_amount'] < 0) | (df['trip_distance'] <= 0)]
    invalid_count = len(invalid_records)
    if invalid_count > 0:
        os.makedirs("../data/logs", exist_ok=True)
        with open(LOG_PATH, "w") as log:
            log.write(f"Removed {invalid_count} invalid records.\n")
            log.write(f"Rows before cleaning: {initial_count}\n")
            log.write(f"Rows after dropna & duplicates: {after_clean_count}\n")
    df = df[(df['fare_amount'] >= 0) & (df['trip_distance'] > 0)]

    # Derived features
    df['trip_speed'] = df['trip_distance'] / (df['trip_duration'] / 60)  # km/h
    df['fare_per_km'] = df['fare_amount'] / df['trip_distance']
    df['pickup_hour'] = pd.to_datetime(df['pickup_datetime']).dt.hour

    # Custom algorithm: flag speed outliers
    df['speed_outlier'] = detect_speed_outliers(df['trip_speed'])

    # Custom algorithm: estimate fare using simplified function
    df['estimated_fare'] = df.apply(
        lambda row: estimate_trip_fare(row['trip_distance'], row['trip_duration'], row['passenger_count']),
        axis=1
    )

    # Peak hours
    peak_hours = identify_peak_hours(df)
    print("Identified peak hours:", peak_hours)

    # Save cleaned CSV
    os.makedirs("../data/cleaned", exist_ok=True)
    df.to_csv(CLEANED_DATA_PATH, index=False)
    print(f"Data cleaned and saved to {CLEANED_DATA_PATH}")
    print("Sample rows:\n", df.head())

if __name__ == "__main__":
    clean_data()
