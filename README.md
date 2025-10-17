# NYCity-Taxi-App 🗽

The NewYorkCity Taxi App is an enterprise-level fullstack application designed to analyse and visualise urban mobility patterns using the New York City Taxi Trip Databaset. It demonstrates data cleaning, storing processed data, backend development, and frontend visualisation of the app. 
## Tech Stack

- Backend API: Python/flask
- Data processing: pandas
- Database: MySQL
- Frontend: HTML, CSS, JavaScript
- version control: Git LFS

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
1. Prerequisites
You must have the following installed:
- python 3.8+
- Node.js and npm
- MySQL server(ensure it's running locally)

### Install Git LFS
`git lfs install`
### clone the repo
`git clone https://github.com/Linda5-umwali/NYCity-Taxi-App.git`

### navigate to the project folder
`cd NYCity-Taxi-App`
### Ensure the large CSV file is downloaded by LFS
`git lfs pull`

### backend
`cd backend`

### Create and activate environment(venv)
`python -m venv venv`
`source venv/bin/activate`

### independencies
`pip install -r requirements.txt`

### Configure Database:

Add your MySQL credentials (replace placeholders with your actual details):

```
[mysql]
host=127.0.0.1
user=your_mysql_user
password=your_mysql_password
database=taxi_db
```

Create the MySQL database named taxi_db manually in your MySQL workbench or client.

Run Data Loading Script: This script will connect to the database, create the necessary table, and load the 279MB data from cleaned_taxi.csv into MySQL.

`python3 data_load.py`

### Run the app
`python3 app.py`

### frontend
`cd NYCity-Taxi-App/frontend`

### Install Node dependencies:

`npm install`

### Launch the React frontend:

`npm start`

The application will automatically open in your browser, typically at http://localhost:3000.

## Dataset

The app uses the official New York City Taxi Trip Dataset, which includes timestamps, distances, durations, pickup/dropoff locations, and other metadata.

## Documentation

- Report (PDF): Explains data cleaning, design decisions, algorithmic logic, and insights. find the doc online here: [https://docs.google.com/document/d/1PyG9kqjDzHFR89xh91mvlmXYHVLleR2Xr8rZ855QgrE/edit?tab=t.0]

- Video Demo: 5-minute walkthrough showing features and architecture. find video here: [![Demo video](https://youtu.be/Ypt1QiUAG4w)]
