import requests


class HttpLayer:
    def post(self, url, data, headers=None, *args, **kwargs):
        raise NotImplementedError()

    def get(self, url, headers=None, *args, **kwargs):
        raise NotImplementedError()

    def head(self, url, headers=None, *args, **kwargs):
        raise NotImplementedError()


class HttpResponse:

    def header(self, header_name):
        raise NotImplementedError()

    @property
    def status_code(self):
        raise NotImplementedError()


#######################################
## Implementations using requests lib

class RequestsHttpLayer(HttpLayer):
    def post(self, url, data, headers=None, *args, **kwargs):
        resp = requests.post(url, data=data, headers=headers, *args, **kwargs)
        return RequestsHttpResponse(resp)

    def get(self, url, headers=None, *args, **kwargs):
        resp = requests.get(url, headers=headers, *args, **kwargs)
        return RequestsHttpResponse(resp)

    def head(self, url, headers=None, *args, **kwargs):
        resp = requests.get(url, headers=headers, *args, **kwargs)
        return RequestsHttpResponse(resp)


class RequestsHttpResponse(HttpResponse):
    def __init__(self, resp):
        self._resp = resp

    def header(self, header_name):
        return self._resp.headers.get(header_name)

    @property
    def status_code(self):
        return self._resp.status_code
