import os
import time

import httpx
from dotenv import load_dotenv
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from src.ingestion.exceptions import (
    PermanentAPIError,
    RetryableAPIError,
)


load_dotenv()


class LinkedInAgentClient:
    def __init__(self):
        self.base_url = os.getenv("API_BASE_URL")
        self.token = os.getenv("API_TOKEN")

        if not self.base_url:
            raise ValueError("API_BASE_URL is not configured.")

        if not self.token:
            raise ValueError("API_TOKEN is not configured.")

    @retry(
        retry=retry_if_exception_type(
            (
                RetryableAPIError,
                httpx.ConnectError,
                httpx.TimeoutException,
                httpx.NetworkError,
            )
        ),
        wait=wait_exponential(
            multiplier=1,
            min=1,
            max=8,
        ),
        stop=stop_after_attempt(4),
        reraise=True,
    )
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

        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")

            if retry_after:
                try:
                    time.sleep(float(retry_after))
                except ValueError:
                    pass

            raise RetryableAPIError(
                "API rate limit exceeded."
            )

        if response.status_code in {
            500,
            502,
            503,
            504,
        }:
            raise RetryableAPIError(
                f"Temporary API failure: HTTP {response.status_code}"
            )

        if 400 <= response.status_code < 500:
            raise PermanentAPIError(
                f"Permanent API failure: HTTP {response.status_code}"
            )

        response.raise_for_status()

        return response.json()