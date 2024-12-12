#!/bin/bash

# Initialize Airflow database if not already initialized
airflow db init

# Start the Airflow webserver
exec airflow webserver
