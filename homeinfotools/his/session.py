"""HIS SSO API."""

from requests import session

from homeinfotools.his.exceptions import DownloadError, LoginError


__all__ = ['HIS_LOGIN_URL', 'HISSession']


HIS_LOGIN_URL = 'https://his.homeinfo.de/session'


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

    def __getattr__(self, attr):
        """Delegates to the session object."""
        return getattr(self.session_guard, attr)

    @property
    def credentials(self):
        """Returns the login credentials as JSON."""
        return {'account': self.account, 'passwd': self.passwd}

    def login(self):
        """Performs a login."""
        response = self.post(HIS_LOGIN_URL, json=self.credentials)

        if response.status_code != 200:
            raise LoginError(response)

        return True

    def get_json(self, url):
        """Returns a JSON-ish dict."""
        response = self.get(url)

        if response.status_code != 200:
            raise DownloadError(response)

        return response.json()
