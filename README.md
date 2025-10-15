# NYCity-Taxi-App 🗽

The NewYorkCity Taxi App is an enterprise-level fullstack application designed to analyse and visualise urban mobility patterns using the New York City Taxi Trip Databaset. It demonstrates data cleaning, storing processed data, backend development, and frontend visualisation of the app. 
## Tech Stack

- Backend: Node.js
- Database: MySQL
- Frontend: HTML, CSS, JavaScript

## Project structure
```
NYCity-Taxi-App/
│
├── backend/
│   ├── app.py                # Flask (or server.js if Node)
│   ├── requirements.txt      # Python dependencies
│   ├── data_processing.py    # data cleaning & feature generation
│   ├── database/
│   │   ├── schema.sql        # DB schema
│   │   └── insert_data.py    # script to insert cleaned data
│   └── api/
│       └── routes.py         # API endpoints
│
├── frontend/
│   ├── index.html
│   ├── styles.css
│   ├── script.js
│   └── assets/               # (optional) charts, icons, etc.
│
├── data/
│   ├── raw/                  # original CSV from train.zip
│   ├── cleaned/              # processed dataset
│   └── logs/                 # invalid or excluded records
│
├── docs/
│   ├── report.pdf            # your final documentation
│   └── architecture-diagram.png
│
├── README.md
└── .gitignore

```

## Setup Instructions
```
# clone the repo
git clone https://github.com/Linda5-umwali/NYCity-Taxi-App.git

# navigate to the project folder
cd NYCity-Taxi-App

# backend
cd backend
pip install -r be.txt

# frontend
cd NYCity-Taxi-App/frontend

# Run the app
python app.py
```

## Dataset

The app uses the official New York City Taxi Trip Dataset, which includes timestamps, distances, durations, pickup/dropoff locations, and other metadata.

## Documentation

- Report (PDF): Explains data cleaning, design decisions, algorithmic logic, and insights. find the doc here: [https://docs.google.com/document/d/1PyG9kqjDzHFR89xh91mvlmXYHVLleR2Xr8rZ855QgrE/edit?usp=sharing]

- Video Demo: 5-minute walkthrough showing features and architecture. find video here: link
