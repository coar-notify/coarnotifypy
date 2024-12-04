"""
Supporting classes for COAR Notify server implementations
"""
import json
import typing
from typing import Union

from coarnotify.factory import COARNotifyFactory

if typing.TYPE_CHECKING:
    from coarnotify.core.notify import NotifyPattern


class COARNotifyReceipt:
    """
    An object representing the response from a COAR Notify server.

    Server implementations should construct and return this object with the appropriate properties
    when implementing the :py:meth:`COARNotifyServiceBinding.notification_received` binding

    :param status: the HTTP status code, should be one of the constants ``CREATED`` (201) or ``ACCEPTED`` (202)
    :param location: the HTTP URI for the resource that was created (if present)
    """

    CREATED = 201
    """The status code for a created resource"""

    ACCEPTED = 202
    """The status code for an accepted request"""

    def __init__(self, status: int, location: str = None):
        """
        Construct a new COARNotifyReceipt object with the status code and location URL (optional)

        :param status: the HTTP status code, should be one of the constants ``CREATED`` (201) or ``ACCEPTED`` (202)
        :param location: the HTTP URI for the resource that was created (if present)
        """
        self._status = status
        self._location = location

    @property
    def status(self) -> int:
        """The status code of the response.  Should be one of the constants ``CREATED`` (201) or ``ACCEPTED`` (202)"""
        return self._status

    @property
    def location(self) -> Union[str, None]:
        """The HTTP URI of the created resource, if present"""
        return self._location


class COARNotifyServiceBinding:
    """
    Interface for implementing a COAR Notify server binding.

    Server implementation should extend this class and implement the :py:meth:`notification_received` method

    That method will receive a :py:class:`NotifyPattern` object, which will be one of the known types
    and should return a :py:class:`COARNotifyReceipt` object with the appropriate status code and location URL
    """

    def notification_received(self, notification: 'NotifyPattern') -> COARNotifyReceipt:
        """
        Process the receipt of the given notification, and respond with an appropriate receipt object

        :param notification: the notification object received
        :return: the receipt object to send back to the client
        """
        raise NotImplementedError()


class COARNotifyServerError(Exception):
    """
    An exception class for server errors in the COAR Notify server implementation.

    The web layer of your server implementation should be able to intercept this from the
    :py:meth:`COARNotifyServer.receive` method and return the appropriate HTTP status code and message to the
    user in its standard way.

    :param status: HTTP Status code to respond to the client with
    :param msg: Message to send back to the client
    """

    def __init__(self, status: int, msg: str):
        """
        Construct a new COARNotifyServerError with the given status code and message

        :param status: HTTP Status code to respond to the client with
        :param msg: Message to send back to the client
        """
        self._status = status
        self._msg = msg
        super(COARNotifyServerError, self).__init__(msg)

    @property
    def status(self) -> int:
        """HTTP status code for the error"""
        return self._status

    @property
    def message(self) -> str:
        """The error message"""
        return self._msg


class COARNotifyServer:
    """
    The main entrypoint to the COAR Notify server implementation.

    The web layer of your application should pass the json/raw payload of any incoming notification to the
    :py:meth:`receive` method, which will parse the payload and pass it to the :py:meth:`COARNotifyServiceBinding.notification_received`
    method of your service implementation

    This object should be constructed with your service implementation passed to it, for example

    .. code-block:: python

        server = COARNotifyServer(MyServiceBinding())
        try:
            response = server.receive(request.json)
            return jsonify(response)
        except COARNotifyServerError as e:
            abort(e.status, e.message)

    :param service_impl: Your service implementation
    """

    def __init__(self, service_impl: COARNotifyServiceBinding):
        """
        Construct a new COARNotifyServer with the given service implementation
        :param service_impl: Your service implementation
        """
        self._service_impl = service_impl

    def receive(self, raw: Union[dict, str], validate: bool = True) -> COARNotifyReceipt:
        """
        Receive an incoming notification as JSON, parse and validate (optional) and then pass to the
        service implementation

        :param raw: The JSON representation of the data, either as a string or a dictionary
        :param validate:    Whether to validate the notification before passing to the service implementation
        :return:   The COARNotifyReceipt response from the service implementation
        """
        if isinstance(raw, str):
            raw = json.loads(raw)

        obj = COARNotifyFactory.get_by_object(raw)
        if validate:
            if not obj.validate():
                raise COARNotifyServerError(400, "Invalid notification")

        return self._service_impl.notification_received(obj)
