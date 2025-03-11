# Deployment Guide

This guide explains how to deploy the wedding website on a production server using Nginx and Gunicorn.

## Server Requirements

- Ubuntu 20.04 LTS or later (or similar Linux distribution)
- Python 3.8 or later
- Nginx
- MongoDB

## Deployment Steps

### 1. Set up the server environment

```bash
# Update package lists
sudo apt update
sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv nginx mongodb

# Start and enable MongoDB
sudo systemctl start mongodb
sudo systemctl enable mongodb

# Create web directory
sudo mkdir -p /var/www/wedding
```

### 2. Clone the repository and set up the application

```bash
# Clone the repository (if using git)
git clone https://your-repository-url.git /tmp/wedding

# Or upload your files to the server using SCP/SFTP

# Copy files to web directory
sudo cp -r /tmp/wedding/* /var/www/wedding/

# Set proper permissions
sudo chown -R www-data:www-data /var/www/wedding
```

### 3. Set up the Python environment and dependencies

```bash
# Create and activate virtual environment
cd /var/www/wedding
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
pip install gunicorn
```

### 4. Configure Nginx

```bash
# Copy the Nginx configuration
sudo cp /var/www/wedding/nginx/wedding.conf /etc/nginx/sites-available/wedding.conf

# Edit the configuration if needed
sudo nano /etc/nginx/sites-available/wedding.conf
# Update server_name with your actual domain name

# Create symbolic link to enable the site
sudo ln -s /etc/nginx/sites-available/wedding.conf /etc/nginx/sites-enabled/

# Test Nginx configuration
sudo nginx -t

# Reload Nginx to apply changes
sudo systemctl reload nginx
```

### 5. Set up Gunicorn service

Create a systemd service file for Gunicorn:

```bash
sudo nano /etc/systemd/system/wedding.service
```

Add the following content:

```ini
[Unit]
Description=Gunicorn instance to serve wedding app
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/wedding
Environment="PATH=/var/www/wedding/venv/bin"
ExecStart=/var/www/wedding/venv/bin/gunicorn --bind 127.0.0.1:5004 app:app

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable wedding.service
sudo systemctl start wedding.service
sudo systemctl status wedding.service
```

### 6. Set up SSL with Let's Encrypt (recommended)

```bash
# Install certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d wedding.example.com

# This will modify your Nginx configuration automatically
```

### 7. Test everything

Visit your domain in a web browser to ensure the website is working properly. Test the RSVP functionality to make sure the API is working.

## Troubleshooting

### Check the logs

```bash
# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Application logs
sudo journalctl -u wedding.service
```

### Restart services

```bash
sudo systemctl restart wedding.service
sudo systemctl reload nginx
```

### Check MongoDB

```bash
mongo
use wedding
db.rsvp.find()
```

## Updating the Website

To update the website with new content:

1. Upload the new files to the server
2. Replace the files in `/var/www/wedding`
3. Restart the application service:

```bash
sudo systemctl restart wedding.service
```
