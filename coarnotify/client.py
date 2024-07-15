import json
from coarnotify.http import RequestsHttpLayer, HttpLayer
from coarnotify.models.notify import NotifyDocument
from coarnotify.exceptions import NotifyException


class NotifyResponse:
    CREATED = "created"
    ACCEPTED = "accepted"

    def __init__(self, action, location=None):
        self._action = action
        self._location = location

    @property
    def action(self):
        return self._action

    @property
    def location(self):
        return self._location


class COARNotifyClient:
    def __init__(self, inbox_url: str = None, http_layer: HttpLayer = None):
        self._inbox_url = inbox_url
        self._http = http_layer if http_layer is not None else RequestsHttpLayer()

    @property
    def inbox_url(self):
        return self._inbox_url

    @inbox_url.setter
    def inbox_url(self, value):
        self._inbox_url = value

    def discover(self, target_url: str):
        # resp = self._http.head(target_url, headers={"Accept": "application/ld+json"})
        # resp = self._http.get(target_url, headers={"Accept": "application/ld+json"})
        # resp = self._http.get(target_url, headers={"Accept": "text/html"})
        pass

    def send(self, notification: NotifyDocument, inbox_url: str = None):
        if inbox_url is None:
            inbox_url = self._inbox_url
        if inbox_url is None:
            raise ValueError("No inbox URL provided")

        resp = self._http.post(inbox_url,
                        data=json.dumps(notification.to_dict()),
                        headers={"Content-Type": "application/ld+json;profile=\"https://www.w3.org/ns/activitystreams\""}
                        )

        if resp.status_code == 201:
            return NotifyResponse(NotifyResponse.CREATED, location=resp.header("Location"))
        elif resp.status_code == 202:
            return NotifyResponse(NotifyResponse.ACCEPTED)

        raise NotifyException("Unexpected response: %s" % resp.status_code)
