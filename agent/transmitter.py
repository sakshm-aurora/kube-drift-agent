# agent/transmitter.py

import requests
import json
import logging
from agent.config import config  # Ensure correct import
import datetime

logging.basicConfig(level=logging.INFO)

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)

class Transmitter:
    def __init__(self):
        self.url = f"{config.central_dashboard_url}/agents/data"
        self.headers = {
            'Authorization': f"Bearer {config.api_key}",
            'Content-Type': 'application/json'
        }

    def send_data(self, data):
        try:
            json_data = json.dumps(data, cls=DateTimeEncoder)
            response = requests.post(self.url, headers=self.headers, data=json_data, timeout=30)
            response.raise_for_status()
            logging.info("Data sent successfully.")
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to send data: {e}")
        except Exception as e:
            logging.error(f"An error occurred during data serialization: {e}")