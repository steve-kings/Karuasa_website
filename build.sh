#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r karuasa/requirements.txt

# Navigate to Django project directory
cd karuasa

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Create superuser if needed (optional - comment out if not needed)
# python manage.py createsuperuser --noinput --username admin --email admin@karuasa.ac.ke || true

echo "Build completed successfully!"
