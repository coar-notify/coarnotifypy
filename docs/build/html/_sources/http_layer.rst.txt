Creating your own HTTP Layer
============================

The HTTP layer is the mechanism by which notifications are sent to the target inbox.  The HTTP layer is designed to be
customisable, so that you can use your own HTTP library, or build in custom authentication routines.

The HTTP layer interface and default implementation can be found in :py:mod:`coarnotify.http`.

To use a custom HTTP layer, you provide this at the time of creating the client:

.. code-block:: python

    from coarnotify.client import COARNotifyClient
    from my_custom_http_layer import MyCustomHTTPLayer

    client = COARNotifyClient(http_layer=MyCustomHTTPLayer())

Implementing HTTP layer with authentication
-------------------------------------------

To add authentication to your http layer, one way of doing this would be to extend the existing ``requests`` based
implementation to layer the authentication on top.

.. code-block:: python

    from coarnotify.http import RequestsHttpLayer
    from requests import HTTPBasicAuth

    class AuthRequestsHTTPLayer(RequestsHttpLayer):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.auth_token = HTTPBasicAuth('username', 'password')

        def post(self, url: str, data: str, headers: dict=None, *args, **kwargs) -> 'RequestsHttpResponse':
            return super().post(url, data, headers=headers, auth=self.auth_token, *args, **kwargs)

        def get(self, url: str, headers: dict=None, *args, **kwargs) -> 'RequestsHttpResponse':
            return super().get(url, data, headers=headers, auth=self.auth_token, *args, **kwargs)


Implementing HTTP layer with alternative library
------------------------------------------------

If your application already relies on another HTTP library, you can implement the HTTP layer using that library instead.

.. code-block:: python

    from coarnotify.http import HttpLayer, HttpResponse
    from my_http_library import MyHttpLibrary


    class MyCustomHTTPLayer(HttpLayer):

        def post(self, url: str, data: str, headers: dict=None, *args, **kwargs) -> 'CustomHttpResponse':
            resp = my_http_library.make_request("POST", url, data, headers=headers, *args, **kwargs)
            return CustomHttpResponse(resp)

        def get(self, url: str, headers: dict=None, *args, **kwargs) -> 'CustomHttpResponse':
            resp = my_http_library.make_request("GET", url, data, headers=headers, *args, **kwargs)
            return CustomHttpResponse(resp)


    class CustomHttpResponse(HttpResponse):
        def __init__(self, resp: my_http_library.Response):
            self._resp = resp

        def header(self, header_name: str) -> str:
            return self._resp.get_response_header(header_name)

        @property
        def status_code(self) -> int:
            return self._resp.get_status_code()