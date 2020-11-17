"""HIS SSO API."""


__all__ = ['WebAPIError', 'DownloadError', 'LoginError']


class WebAPIError(Exception):
    """A web API error."""

    def __init__(self, response):
        """Sets the response."""
        super().__init__(response)
        self.response = response

    def __str__(self):
        """Returns the content as string."""
        return self.response.text


class DownloadError(WebAPIError):
    """Indicates an error during data download."""


class LoginError(WebAPIError):
    """Indicates an error during login."""
