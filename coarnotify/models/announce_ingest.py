from typing import Union

from coarnotify.models.notify import NotifyDocument
from coarnotify.activitystreams.activitystreams import ActivityStream


class AnnounceIngest(NotifyDocument):
    TYPE = ["Announce", "coar-notify:IngestAction"]
    IDENTIFY_BY_TYPE = [
        TYPE
    ]

    def __init__(self, stream: Union[ActivityStream, dict] = None):
        super(AnnounceIngest, self).__init__(stream=stream)