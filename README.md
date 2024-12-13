# Data Engineering Project: Reddit Data Analysis

This project processes Reddit data, stores it in a database, and provides analysis through scripts. It is containerized using Docker and follows best practices in data engineering.

## Project Structure

### Main Files

- **`.env`**: Configuration file storing environment variables such as database credentials.
- **`app.py`**: Main application script to manage and orchestrate data operations.
- **`docker-compose.yml`**: Docker Compose configuration to set up services like the database and application.
- **`Dockerfile`**: Instructions to build the Docker image for this project.
- **`entrypoint.sh`**: Script to initialize and configure the container environment.
- **`extract_load.py`**: Script to extract and load data from a source into the database.
- **`init.sql`**: SQL file to initialize database schemas and tables.
- **`reddit_etl.py`**: ETL script to extract, transform, and load Reddit data.
- **`requirements.txt`**: Python dependencies required for the project.
- **`test.py`**: Script to test various functionalities of the project.
- **`top_subreddits.csv`**: CSV file containing preprocessed data about top subreddits.

## Features

### 1. **ETL Pipeline**
- **Extraction**: Extracts data from Reddit API or CSV files.
- **Transformation**: Processes and cleans the data.
- **Loading**: Stores the data into a PostgreSQL database.

### 2. **Database Initialization**
- Creates necessary tables and schemas using `init.sql`.
- Configured via `docker-compose.yml` for seamless setup.

### 3. **Data Analysis**
- Supports analysis and visualization of Reddit data.
- Scripts like `app.py` and `reddit_etl.py` provide functionalities to process and display insights.

### 4. **Containerized Deployment**
- Uses Docker for portability and consistency.
- `docker-compose.yml` simplifies multi-service setup.

### 5. **Testing**
- Includes `test.py` to validate data processing and database interactions.

## Setup and Usage

### Prerequisites
- Install [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/).

## Scripts

### `app.py`
- This script acts as the entry point for orchestrating all project functionalities.
- Responsibilities:
  - **Data Access**: Fetches data from the PostgreSQL database.
  - **Data Transformation**: Normalizes and prepares data for visualization.
  - **Visualization**: Displays insights using visualizations like histograms and bar charts.
- Outputs:
  - Provides interactive dashboards for users to explore data insights and trends.

### `reddit_etl.py`
- A core ETL (Extract, Transform, Load) pipeline designed for Reddit data.
- **Details**:
  - **Extraction**:
    - Connects to the Reddit API using credentials to fetch subreddit information.
    - Supports data ingestion from predefined CSVs for offline testing.
  - **Transformation**:
    - Cleans raw data by removing duplicates, handling missing values, and standardizing fields.
    - Calculates relevant metrics like subreddit activity trends.
  - **Loading**:
    - Inserts processed data into a PostgreSQL database.
- Outputs:
  - Structured and cleaned subreddit data stored in the database for further use.

### `extract_load.py`
- Simplifies data ingestion tasks by focusing on extracting and loading data.
- **Details**:
  - Works with local files or external APIs to fetch raw data.
  - Minimal transformations applied to ensure format consistency.
  - Uses modular functions for reusability.
- Outputs:
  - Loads data directly into PostgreSQL tables, ready for further transformations.

### `test.py`
- Ensures the integrity and reliability of the ETL pipeline and database.
- **Details**:
  - Validates database schema consistency with `init.sql`.
  - Tests the functionality of extraction and transformation steps.
  - Simulates edge cases like missing fields or network failures to check error handling.
- Outputs:
  - Logs results of all test cases, highlighting failures and coverage gaps.

## File Details

### `requirements.txt`
Dependencies for the project:
- `streamlit`: For building interactive web applications.
- `pandas`: For data manipulation and analysis.
- `psycopg2`: For connecting to and interacting with the PostgreSQL database.
- `requests`: For making HTTP requests to fetch data from APIs.
- `sqlalchemy`: For database ORM and management.
- `matplotlib`: For creating data visualizations.
- `beautifulsoup4`: For parsing HTML content during data extraction.

### `top_subreddits.csv`
- A CSV file containing sample data about top subreddits.
- Used as an initial dataset for testing and demonstration purposes.

## Future Enhancements
- Implement advanced analytics and visualizations.
- Extend the ETL pipeline for real-time data processing.
- Add more test cases for comprehensive coverage.





