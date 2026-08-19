import os

import httpx
from dotenv import load_dotenv


load_dotenv()


class LinkedInAgentClient:
    def __init__(self):
        self.base_url = os.getenv("API_BASE_URL")
        self.token = os.getenv("API_TOKEN")

        if not self.base_url:
            raise ValueError("API_BASE_URL is not configured.")

        if not self.token:
            raise ValueError("API_TOKEN is not configured.")

    def get(self, endpoint, params=None):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
        }

        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        response = httpx.get(
            url,
            headers=headers,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()