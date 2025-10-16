# NYCity-Taxi-App 🗽

The NewYorkCity Taxi App is an enterprise-level fullstack application designed to analyse and visualise urban mobility patterns using the New York City Taxi Trip Databaset. It demonstrates data cleaning, storing processed data, backend development, and frontend visualisation of the app. 
## Tech Stack

- Backend: Node.js
- Data processing: python
- Database: MySQL
- Frontend: HTML, CSS, JavaScript

## Project structure
```
NYCity-Taxi-App/
│
├── backend/
│   ├── app.py 
│   ├── requirements.txt
│   ├── data_processing.py
│   ├── database/
│   │   ├── schema.sql
│   │   └── insert_data.py
│   └── api/
│       └── routes.py
│
├── frontend/
│   └── index.html
│
├── data/
│   ├── raw/                 
│   ├── cleaned/
│   │   └── cleaned_taxi.csv
│   └── logs/
│       └── cleaning_log.csv
├── NYC Taxi Data                # PDF report
├── README.md
└── .gitignore

```

## Setup Instructions
```
# clone the repo
git clone https://github.com/Linda5-umwali/NYCity-Taxi-App.git

# navigate to the project folder
cd NYCity-Taxi-App

# Create and activate environment(venv)
python -m venv venv
source venv/bin/activate

# independencies
pip install -r requirements.txt

# backend
cd backend
python db_data.py

# frontend
cd NYCity-Taxi-App/frontend

# Run the app
python3 app.py
```

## Dataset

The app uses the official New York City Taxi Trip Dataset, which includes timestamps, distances, durations, pickup/dropoff locations, and other metadata.

## Documentation

- Report (PDF): Explains data cleaning, design decisions, algorithmic logic, and insights. find the doc online here: [https://docs.google.com/document/d/1PyG9kqjDzHFR89xh91mvlmXYHVLleR2Xr8rZ855QgrE/edit?tab=t.0]

- Video Demo: 5-minute walkthrough showing features and architecture. find video here: [video]
