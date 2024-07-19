from typing import Union

from coarnotify.models.notify import NotifyDocument
from coarnotify.activitystreams2.activitystreams2 import ActivityStream


class AnnounceServiceResult(NotifyDocument):
    TYPE = "Announce"

    def __init__(self, stream: Union[ActivityStream, dict] = None):
        super(AnnounceServiceResult, self).__init__(stream=stream)