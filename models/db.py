from flask import Flask
import tortilla

from requests.adapters import HTTPAdapter
from requests.packages.urllib3 import Retry
from tortilla import formats

from models.formatters import setup_format_str

app = Flask(__name__)
app.config.from_pyfile('../config.py')


class TortillaEntity(object):
    base_url = None
    suffix = None

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
        path = "/".join([self._get_path_value(path) for path in path_list])
        if self.suffix:
            path += self.suffix
        return path

    def _get_path(self):
        path = []
        for base in list(self.__class__.__bases__)[::-1] + [self.__class__]:
            if hasattr(base, "path"):
                path.extend(base.path)
        return path

    @staticmethod
    def _get_path_value(path_item):
        if not isinstance(path_item, Param):
            return path_item
        if path_item.value:
            return str(path_item.value)
        return path_item.get_format_str()

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
        kwargs['params'] = self._get_auth()
        kwargs['format'] = ('json', 'str')
        self.body = self.request.post(*args, **kwargs)
        return self.body

    def __getattr__(self, item):
        if item == 'request':
            return self.api


class Param(object):
    _value = None

    def __init__(self, name):
        self.name = name
        super(Param, self).__init__()

    def get_format_str(self):
        return "{%s}" % self.name

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, x):
        self._value = x

    def __cmp__(self, other):
        return __cmp__(self._value, other)


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


class Categories(Index):
    path = [
        'category.json'
    ]

    def get_with_rooms(self):
        return self.get(params={'depth': 1})


class SingleRoom(Index):
    room_id = Param('room_id')
    path = [
        'room',
        'id',
        room_id
    ]

    suffix = '.json'

    def __init__(self, room_id):
        self.room_id.value = room_id
        super(SingleRoom, self).__init__()