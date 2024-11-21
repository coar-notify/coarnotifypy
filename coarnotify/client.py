"""
This module contains all the client-specific code for sending notifications
to an inbox and receiving the responses it may return
"""

import json
from typing import Union

from coarnotify.exceptions import NotifyException
from coarnotify.http import RequestsHttpLayer, HttpLayer
from coarnotify.core.notify import NotifyPattern


class NotifyResponse:
    """
    An object representing the response from a COAR Notify inbox.

    This contains the action that was carried out on the server:

    * CREATED - a new resource was created

    * ACCEPTED - the request was accepted, but the resource was not yet created

    In the event that the resource is created, then there will also be a location
    URL which will give you access to the resource
    """
    CREATED = "created"
    ACCEPTED = "accepted"

    def __init__(self, action, location=None):
        """
        Construct a new NotifyResponse object with the action (created or accepted) and the location URL (optional)

        :param action: The action which the server said it took
        :param location: The HTTP URI for the resource that was created (if present)
        """
        self._action = action
        self._location = location

    @property
    def action(self) -> str:
        """The action that was taken, will be one of the constants CREATED or ACCEPTED"""
        return self._action

    @property
    def location(self) -> Union[str, None]:
        """The HTTP URI of the created resource, if present"""
        return self._location


class COARNotifyClient:
    """
    The COAR Notify Client, which is the mechanism through which you will interact with external inboxes.

    If you do not supply an inbox URL at construction you will
    need to supply it via the ``inbox_url`` setter, or when you send a notification

    :param inbox_url:   HTTP URI of the inbox to communicate with by default
    :param http_layer:  An implementation of the HttpLayer interface to use for sending HTTP requests.
                        If not provided, the default implementation will be used based on ``requests``
    """
    def __init__(self, inbox_url: str = None, http_layer: HttpLayer = None):
        self._inbox_url = inbox_url
        self._http = http_layer if http_layer is not None else RequestsHttpLayer()

    @property
    def inbox_url(self) -> Union[str, None]:
        """The HTTP URI of the inbox to communicate with by default"""
        return self._inbox_url

    @inbox_url.setter
    def inbox_url(self, value: str):
        """Set the HTTP URI of the inbox to communicate with by default"""
        self._inbox_url = value

    def send(self, notification: NotifyPattern, inbox_url: str = None, validate: bool = True) -> NotifyResponse:
        """
        Send the given notification to the inbox.  If no inbox URL is provided, the default inbox URL will be used.

        :param notification: The notification object (from the models provided, or a subclass you have made of the NotifyPattern class)
        :param inbox_url: The HTTP URI to send the notification to.  Omit if using the default inbox_url supplied in the constructor.
                            If it is omitted, and no value is passed here then we will also look in the ``target.inbox`` property of the notification
        :param validate: Whether to validate the notification before sending.  If you are sure the notification is valid, you can set this to False
        :return: a NotifyResponse object representing the response from the server
        """
        if inbox_url is None:
            inbox_url = self._inbox_url
        if inbox_url is None:
            inbox_url = notification.target.inbox
        if inbox_url is None:
            raise ValueError("No inbox URL provided at the client, method, or notification level")

        if validate:
            if not notification.validate():
                raise NotifyException("Attempting to send invalid notification; to override set validate=False when calling this method")

        resp = self._http.post(inbox_url,
                        data=json.dumps(notification.to_jsonld()),
                        headers={"Content-Type": "application/ld+json;profile=\"https://www.w3.org/ns/activitystreams\""}
                        )

        if resp.status_code == 201:
            return NotifyResponse(NotifyResponse.CREATED, location=resp.header("Location"))
        elif resp.status_code == 202:
            return NotifyResponse(NotifyResponse.ACCEPTED)

        raise NotifyException("Unexpected response: %s" % resp.status_code)
