import json
from coarnotify.http import RequestsHttpLayer, HttpLayer
from coarnotify.models.notify import Notify
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
    def __init__(self, http_layer: HttpLayer = None):
        self._http = http_layer if http_layer is not None else RequestsHttpLayer()

    def discover(self, target_url: str):
        # resp = self._http.head(target_url, headers={"Accept": "application/ld+json"})
        # resp = self._http.get(target_url, headers={"Accept": "application/ld+json"})
        # resp = self._http.get(target_url, headers={"Accept": "text/html"})
        pass

    def send(self, inbox_url: str, notification: Notify):
        resp = self._http.post(inbox_url,
                        data=json.dumps(notification.to_dict()),
                        headers={"Content-Type": "application/ld+json;profile=\"https://www.w3.org/ns/activitystreams\""}
                        )

        if resp.status_code == 201:
            return NotifyResponse(NotifyResponse.CREATED, location=resp.header("Location"))
        elif resp.status_code == 202:
            return NotifyResponse(NotifyResponse.ACCEPTED)

        raise NotifyException("Unexpected response: %s" % resp.status_code)
