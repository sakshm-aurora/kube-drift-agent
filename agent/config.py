# agent/config.py

import os

class Config:
    def __init__(self):
        self.central_dashboard_url = os.getenv('CENTRAL_DASHBOARD_URL', 'http://host.docker.internal:8000')
        self.api_key = os.getenv('API_KEY', 'test-api-key')
        self.include_secrets_option = os.getenv('INCLUDE_SECRETS_OPTION', 'exclude')
        # Options: 'exclude', 'metadata', 'hashed'

config = Config()