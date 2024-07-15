from typing import Union

from coarnotify.models.notify import NotifyDocument
from coarnotify.activitystreams.activitystreams import ActivityStream


class AnnounceReview(NotifyDocument):
    TYPE = ["Announce", "coar-notify:ReviewAction"]

    def __init__(self, stream: Union[ActivityStream, dict] = None):
        super(AnnounceReview, self).__init__(stream=stream)