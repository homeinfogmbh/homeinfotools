"""HIS SSO API."""

from typing import Any

from requests import session

from homeinfotools.his.exceptions import DownloadError, LoginError


__all__ = ['HISSession']


URL = 'https://his.homeinfo.de/session'


class HISSession:
    """A HIS session."""

    def __init__(self, account: str, passwd: str):
        """Sets account name and password."""
        self.account = account
        self.passwd = passwd
        self.session = session()
        self.session_guard = None

    def __enter__(self):
        self.session_guard = self.session.__enter__()
        self.login()
        return self

    def __exit__(self, *args):
        self.session_guard = None
        return self.session.__exit__(*args)

    def __getattr__(self, attr: str) -> Any:
        """Delegates to the session object."""
        return getattr(self.session_guard, attr)

    @property
    def json(self):
        """Returns the login credentials as JSON."""
        return {'account': self.account, 'passwd': self.passwd}

    def login(self) -> bool:
        """Performs a login."""
        if (response := self.post(URL, json=self.json)).status_code != 200:
            raise LoginError(response)

        return True

    def get_json(self, url: str) -> dict | list:
        """Returns a JSON-ish dict."""
        if (response := self.get(url)).status_code != 200:
            raise DownloadError(response)

        return response.json()
