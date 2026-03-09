#!/bin/sh

# This line makes the script exit immediately if any command fails
set -e

# Run the database migrations
echo "Applying database migrations..."
python manage.py migrate

# Start the Gunicorn web server
# 'exec' replaces the script process with the Gunicorn process
echo "Starting Gunicorn server..."
exec python -m gunicorn --bind 0.0.0.0:8080 --workers 2 config.wsgi:application