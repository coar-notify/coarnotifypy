from typing import Union

from coarnotify.models.notify import NotifyDocument
from coarnotify.activitystreams2.activitystreams2 import ActivityStream


class AnnounceIngest(NotifyDocument):
    TYPE = ["Announce", "coar-notify:IngestAction"]

    def __init__(self, stream: Union[ActivityStream, dict] = None):
        super(AnnounceIngest, self).__init__(stream=stream)