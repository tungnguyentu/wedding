# Wedding Website

## Description
Wedding website with RSVP functionality. Built with Flask backend and static HTML/CSS/JS frontend.

## Prerequisites
- Python 3.7+
- Nginx
- MongoDB

## Local Development

### Setup the Backend

1. Create a virtual environment and install dependencies:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Mac/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

2. Run the Flask backend:

```bash
# Using Flask development server
python app.py

# OR using the start script
./start.sh

# OR using Gunicorn (more like production environment)
./start.sh gunicorn
```

This will start the server at http://localhost:5004.

### Serve the Frontend

For local development, you can use a simple HTTP server:

```bash
# Using Python 3:
python -m http.server 8000
```

Then access the website at http://localhost:8000.

## Production Deployment

For production deployment on a server:

1. See [DEPLOY.md](DEPLOY.md) for detailed instructions on setting up Nginx and deploying to a production server.

2. The application is designed to run with:
   - Static files served by Nginx
   - API requests proxied to a Gunicorn instance running the Flask application
   - MongoDB database for storing RSVP responses

### Using Gunicorn

Gunicorn (Green Unicorn) is a Python WSGI HTTP Server for UNIX. It's a pre-fork worker model, ported from Ruby's Unicorn project. It supports various worker types and is designed to be robust for production environments.

To run the application with Gunicorn:

```bash
# Using the configuration file
gunicorn --config gunicorn_config.py app:app

# OR directly from command line
gunicorn --bind 127.0.0.1:5004 app:app --workers 3
```

## Export RSVP Data to CSV

To export RSVP data to CSV:

```bash
python export_to_csv.py
```

This will generate an `rsvp_data.csv` file with all the RSVP responses from the MongoDB database.

## Project Structure
- `app.py` - Flask backend for handling RSVP submissions
- `export_to_csv.py` - Utility to export RSVP data to CSV
- `index.html` - Main wedding website
- `nginx/` - Nginx configuration for production deployment
- `requirements.txt` - Python dependencies
- `gunicorn_config.py` - Configuration for Gunicorn WSGI server
- `start.sh` - Helper script to start the application

## Next Steps
1. Define project requirements
2. Create necessary files and directories
3. Update this README with specific instructions

## Contributing
Please reach out to the repository owner for contribution guidelines.