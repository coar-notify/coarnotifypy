from coarnotify.http import HttpLayer, HttpResponse


class MockHttpLayer(HttpLayer):
    def __init__(self, status_code=200, location=None):
        self._status_code = status_code
        self._location = location

    def post(self, url, data, headers=None, *args, **kwargs):
        return MockHttpResponse(status_code=self._status_code, location=self._location)

    def get(self, url, headers=None, *args, **kwargs):
        raise NotImplementedError()

    def head(self, url, headers=None, *args, **kwargs):
        raise NotImplementedError()


class MockHttpResponse(HttpResponse):
    def __init__(self, status_code=200, location=None):
        self._status_code = status_code
        self._location = location

    def header(self, header_name):
        if header_name.lower() == "location":
            return self._location

    @property
    def status_code(self):
        return self._status_code