"""
HTTP layer interface and default implementation using requests lib
"""
import requests


class HttpLayer:
    """
    Interface for the HTTP layer

    This defines the methods which need to be implemented in order for the client to fully operate
    """

    def post(self, url: str, data: str, headers: dict=None, *args, **kwargs) -> 'HttpResponse':
        """
        Make an HTTP POST request to the supplied URL with the given body data, and headers

        `args` and `kwargs` can be used to pass implementation-specific parameters

        :param url: the request URL
        :param data: the body data
        :param headers: HTTP headers as a dict to include in the request
        :param args: argument list to pass on to the implementation
        :param kwargs: keyword arguments to pass on to the implementation
        :return: HttpResponse
        """
        raise NotImplementedError()

    def get(self, url: str, headers: dict=None, *args, **kwargs) -> 'HttpResponse':
        """
        Make an HTTP GET request to the supplied URL with the given headers

        `args` and `kwargs` can be used to pass implementation-specific parameters

        :param url: the request URL
        :param headers: HTTP headers as a dict to include in the request
        :param args: argument list to pass on to the implementation
        :param kwargs: keyword arguments to pass on to the implementation
        :return: HttpResponse
        """
        raise NotImplementedError()


class HttpResponse:
    """
    Interface for the HTTP response object

    This defines the methods which need to be implemented in order for the client to fully operate
    """

    def header(self, header_name: str) -> str:
        """
        Get the value of a header from the response

        :param header_name: the name of the header
        :return: the header value
        """
        raise NotImplementedError()

    @property
    def status_code(self) -> int:
        """
        Get the status code of the response

        :return: the status code
        """
        raise NotImplementedError()


#######################################
## Implementations using requests lib

class RequestsHttpLayer(HttpLayer):
    """
    Implementation of the HTTP layer using the requests library.  This is the default implementation
    used when no other implementation is supplied
    """

    def post(self, url: str, data: str, headers: dict=None, *args, **kwargs) -> 'RequestsHttpResponse':
        """
        Make an HTTP POST request to the supplied URL with the given body data, and headers

        `args` and `kwargs` can be used to pass additional parameters to the `requests.post` method,
        such as authentication credentials, etc.

        :param url: the request URL
        :param data: the body data
        :param headers: HTTP headers as a dict to include in the request
        :param args: argument list to pass on to requests.post
        :param kwargs: keyword arguments to pass on to requests.post
        :return: RequestsHttpResponse
        """
        resp = requests.post(url, data=data, headers=headers, *args, **kwargs)
        return RequestsHttpResponse(resp)

    def get(self, url: str, headers: dict=None, *args, **kwargs) -> 'RequestsHttpResponse':
        """
        Make an HTTP GET request to the supplied URL with the given headers

        `args` and `kwargs` can be used to pass additional parameters to the `requests.get` method,
        such as authentication credentials, etc.

        :param url: the request URL
        :param headers: HTTP headers as a dict to include in the request
        :param args: argument list to pass on to requests.get
        :param kwargs: keyword arguments to pass on to requests.get
        :return: HttpResponse
        """

        resp = requests.get(url, headers=headers, *args, **kwargs)
        return RequestsHttpResponse(resp)

class RequestsHttpResponse(HttpResponse):
    """
    Implementation fo the HTTP response object using the requests library

    This wraps the requests response object and provides the interface required by the client

    :param resp: response object from the requests library
    """

    def __init__(self, resp: requests.Response):
        """
        Construct the object as a wrapper around the original requests response object

        :param resp: response object from the requests library
        """
        self._resp = resp

    def header(self, header_name: str) -> str:
        """
        Get the value of a header from the response

        :param header_name: the name of the header
        :return: the header value
        """
        return self._resp.headers.get(header_name)

    @property
    def status_code(self) -> int:
        """
        Get the status code of the response

        :return: the status code
        """
        return self._resp.status_code

    @property
    def requests_response(self) -> requests.Response:
        """Get the original requests response object"""
        return self._resp
