class RetryableAPIError(Exception):
    """Raised when an API response indicates a temporary failure."""


class PermanentAPIError(Exception):
    """Raised when an API response should not be retried."""