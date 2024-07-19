from typing import Union

from coarnotify.models.notify import NotifyDocument
from coarnotify.activitystreams2.activitystreams2 import ActivityStream


class Reject(NotifyDocument):
    TYPE = "Reject"

    def __init__(self, stream: Union[ActivityStream, dict] = None):
        super(Reject, self).__init__(stream=stream)

