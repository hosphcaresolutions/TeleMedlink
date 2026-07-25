#!/usr/bin/env bash
set -o errexit  # Exit on error

pip install -r requirements.txt
pip install -r requirements.render.txt
python manage.py collectstatic --no-input
python manage.py migrate --no-input
