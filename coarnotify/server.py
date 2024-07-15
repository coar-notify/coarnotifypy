from coarnotify.models import NotifyDocument
from coarnotify.common import COARNotifyFactory


class COARNotifyReceipt:
    CREATED = 201
    ACCEPTED = 202

    def __init__(self, status, location=None):
        self._status = status
        self._location = location

    @property
    def status(self):
        return self._status

    @property
    def location(self):
        return self._location


class COARNotifyServiceBinding:
    def notification_received(self, notification: NotifyDocument) -> COARNotifyReceipt:
        raise NotImplementedError()


class COARNotifyServerError(Exception):
    def __init__(self, status, msg):
        self._status = status
        self._msg = msg
        super(COARNotifyServerError, self).__init__(msg)

    @property
    def status(self):
        return self._status

    @property
    def message(self):
        return self._msg


class COARNotifyServer:
    def __init__(self, service_impl):
        self._service_impl = service_impl

    def receive(self, raw, validate=True):
        obj = COARNotifyFactory.get_by_object(raw)
        if validate:
            if not obj.validate():
                raise COARNotifyServerError(400, "Invalid notification")

        return self._service_impl.notification_received(obj)