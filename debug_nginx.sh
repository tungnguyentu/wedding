#!/bin/bash

echo "===== NGINX CONFIGURATION TEST ====="
sudo nginx -t

echo
echo "===== NGINX ENABLED SITES ====="
ls -l /etc/nginx/sites-enabled/

echo
echo "===== NGINX ERROR LOG (LAST 20 LINES) ====="
sudo tail -n 20 /var/log/nginx/error.log

echo
echo "===== NGINX ACCESS LOG (LAST 20 LINES) ====="
sudo tail -n 20 /var/log/nginx/access.log

echo
echo "===== CHECKING API CONNECTION ====="
curl -I http://127.0.0.1:5004/api/content

echo
echo "===== TESTING NGINX PROXY ====="
curl -I -H "X-User-ID: 123ccc9e" http://localhost/api/content

echo
echo "===== PORT STATUS ====="
sudo netstat -tulpn | grep -E '5004|80'

echo
echo "===== GUNICORN STATUS ====="
sudo systemctl status wedding.service --no-pager
