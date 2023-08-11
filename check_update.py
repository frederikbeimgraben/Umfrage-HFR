#!/usr/bin/env python3
"""
Check if a new commit has been made to github.com/frederikbeimgraben/jagdmodelle-umfrage and
if so, pull the changes, build the node server and restart the services.
"""

# Imports
import os
import subprocess
import sys
import json
import requests
import time

# Constants
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# Remote repository
REMOTE = 'frederikbeimgraben/Umfrage-HFR'

# Executable Deployment file
DEPLOY = os.path.join(BASE_PATH, 'jagdmodelle-umfrage', 'deploy')

# Restart services executable
SERVICES = os.path.join(BASE_PATH, 'services', 'make_services')

# Get the current commit hash
CURRENT_COMMIT_HASH = subprocess.check_output(
    ['git', 'rev-parse', 'HEAD'],
    cwd=BASE_PATH
).decode('utf-8').strip()

while True:    
    # Get the latest commit hash
    LATEST_COMMIT_HASH = requests.get(
        f'https://api.github.com/repos/{REMOTE}/commits/main'
    ).json()['sha']
    
    # Check if the latest commit hash is different from the current commit hash
    if CURRENT_COMMIT_HASH != LATEST_COMMIT_HASH:
        print('New commit found. Updating server...')
        
        # Pull the latest changes
        subprocess.check_call(
            ['git', 'pull'],
            cwd=BASE_PATH
        )
        
        # Build the node server
        subprocess.check_call(
            [DEPLOY],
            cwd=os.path.join(BASE_PATH, 'jagdmodelle-umfrage')
        )
        
        # Restart the services
        subprocess.check_call(
            ['sudo', SERVICES],
            cwd=os.path.join(BASE_PATH, 'services')
        )
        
        # Restart own service
        subprocess.check_call(
            ['sudo', 'systemctl', 'restart', 'jagdmodelle-check-update.service'],
            cwd=os.path.join(BASE_PATH, 'services')
        )
        
        # Get the new commit hash
        CURRENT_COMMIT_HASH = LATEST_COMMIT_HASH
        
        print('Successfully updated the server.')
    
    # Wait 5 minutes
    time.sleep(300)