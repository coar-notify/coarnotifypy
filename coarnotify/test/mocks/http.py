"""Mocks for the HTTP layer and HTTP response objects."""

from coarnotify.http import HttpLayer, HttpResponse


class MockHttpLayer(HttpLayer):
    """Mock HTTP layer for testing."""

    def __init__(self, status_code=200, location=None):
        """Construct a new MockHttpLayer object."""
        self._status_code = status_code
        self._location = location

    def post(self, url, data, headers=None, *args, **kwargs):
        """Mock the POST method."""
        return MockHttpResponse(status_code=self._status_code, location=self._location)

    def get(self, url, headers=None, *args, **kwargs):
        """Mock the GET method."""
        raise NotImplementedError()

    def head(self, url, headers=None, *args, **kwargs):
        """Head not implemented."""
        raise NotImplementedError()


class MockHttpResponse(HttpResponse):
    """Mock HTTP response object."""

    def __init__(self, status_code=200, location=None):
        """Construct a new MockHttpResponse object."""
        self._status_code = status_code
        self._location = location

    def header(self, header_name):
        """Return the value of the given header."""
        if header_name.lower() == "location":
            return self._location

    @property
    def status_code(self):
        """Return the status code."""
        return self._status_code
