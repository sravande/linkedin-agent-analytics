import os
import time

import httpx
from dotenv import load_dotenv
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

load_dotenv()


class LinkedInAgentClient:

    def __init__(self):
        self.base_url = os.getenv("API_BASE_URL")
        self.token = os.getenv("API_TOKEN")

        if not self.base_url:
            raise ValueError("API_BASE_URL is not configured")

        if not self.token:
            raise ValueError("API_TOKEN is not configured")

    @retry(
        stop=stop_after_attempt(4),
        wait=wait_exponential(
            multiplier=2,
            min=2,
            max=8,
        ),
        retry=retry_if_exception_type(
            (httpx.RequestError, httpx.HTTPStatusError)
        ),
        reraise=True,
    )
    def get(self, endpoint, params=None):

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
        }

        response = httpx.get(
            f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}",
            headers=headers,
            params=params,
            timeout=30,
        )

        if response.status_code == 429:

            retry_after = response.headers.get("Retry-After")

            if retry_after:
                time.sleep(float(retry_after))

            response.raise_for_status()

        response.raise_for_status()

        return response.json()