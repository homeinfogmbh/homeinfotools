"""Common exceptions."""

__all__ = ['LoginError']


class WebAPIError(Exception):
    """A web API error."""

    def __init__(self, response):
        """Sets the response."""
        super().__init__(response)
        self.response = response

    def __str__(self):
        """Returns the content as string."""
        return self.response.text


class LoginError(WebAPIError):
    """Indicates an error during login."""


class DownloadError(WebAPIError):
    """Indicates an error during data download."""
