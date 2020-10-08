"""Common exceptions."""

__all__ = ['LoginError']


class WebAPIError(Exception):
    """A web API error."""

    def __init__(self, content):
        """Sets the content."""
        super().__init__(content)
        self.content = content

    def __str__(self):
        """Returns the content as string."""
        if content := self.content is None:
            return ''

        try:
            return content.decode()
        except UnicodeDecodeError:
            return str(content)


class LoginError(WebAPIError):
    """Indicates an error during login."""


class DownloadError(WebAPIError):
    """Indicates an error during data download."""
