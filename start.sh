#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Check if the user wants to run with Gunicorn
if [ "$1" == "gunicorn" ]; then
  echo "Starting with Gunicorn..."
  if [ -f "gunicorn_config.py" ]; then
    gunicorn --config gunicorn_config.py app:app
  else
    gunicorn --bind 127.0.0.1:5004 app:app --workers 3
  fi
else
  # Run with Flask's development server
  echo "Starting with Flask development server..."
  python app.py
fi
