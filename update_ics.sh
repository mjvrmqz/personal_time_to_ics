#!/bin/bash

# Go to the folder where this script is located
cd "$(dirname "$0")"

# Load environment variables from .env
if [ -f .env ]; then
    set -o allexport
    source .env
    set +o allexport
fi

# Run the Python script that updates the ICS file
python3 personal_time_to_ics.py

# Add changes to git and push
git add personal_time_feed.ics
git commit -m "Auto-update personal time ICS feed $(date)" || true
git pull --rebase
git push