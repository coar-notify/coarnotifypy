from typing import Union

from coarnotify.models.notify import NotifyDocument
from coarnotify.activitystreams2.activitystreams2 import ActivityStream


class Accept(NotifyDocument):
    TYPE = "Accept"

    def __init__(self, stream: Union[ActivityStream, dict] = None):
        super(Accept, self).__init__(stream=stream)

