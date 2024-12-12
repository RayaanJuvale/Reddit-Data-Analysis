# Use a slim Python image for a smaller container size
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install praw explicitly (in case it's missing from requirements.txt)
RUN pip install praw

# Copy the application code into the container
COPY . /app

# Allow setting the command dynamically for streamlit or etl
# Default to running the ETL script (can be overridden in docker-compose)
CMD ["python", "reddit_etl.py"]
