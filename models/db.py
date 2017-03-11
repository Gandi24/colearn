from flask import Flask
import tortilla

from requests.adapters import HTTPAdapter
from requests.packages.urllib3 import Retry

app = Flask(__name__)
app.config.from_pyfile('../config.py')


class TortillaEntity(object):
    base_url = None

    def __init__(self, **kwargs):
        self.url = self._get_url()
        self.api = tortilla.wrap(self.url, headers=self.headers)
        self._client.session.mount('http://',
                                   HTTPAdapter(max_retries=Retry(total=5)))
        self.body = None

    def _get_url(self):
        if not self.base_url:
            raise NotImplementedError("Make sure to assign base_url first")
        path_list = [self.base_url.strip("/")] + self._get_path()
        return "/".join(path_list)

    def _get_path(self):
        path = []
        for base in list(self.__class__.__bases__)[::-1] + [self.__class__]:
            if hasattr(base, "path"):
                path.extend(base.path)
        return path

    def _get_auth(self):
        return {
            'apikey': app.config['API_KEY']
        }

    @property
    def headers(self):
        return None

    @property
    def _client(self):
        return self.api._parent

    def get(self, params=None):
        request_params = self._get_auth()
        if isinstance(params, dict):
            request_params.update(params)
        self.body = self.request.get(params=request_params)
        return self.body

    def post(self, *args, **kwargs):
        self.body = self.request.post(*args, **kwargs)
        return self.body

    def __getattr__(self, item):
        if item == 'request':
            return self.api


class DB(TortillaEntity):
    base_url = app.config['DATABASE_URI']


class Index(DB):
    path = [
        "db",
        "team1"
    ]


class Rooms(Index):
    path = [
        "room.json"
    ]