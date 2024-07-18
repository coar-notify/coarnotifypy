from typing import Union

from coarnotify.models.notify import NotifyDocument
from coarnotify.activitystreams2.activitystreams2 import ActivityStream


class AnnounceEndorsement(NotifyDocument):
    TYPE = ["Announce", "coar-notify:EndorsementAction"]

    def __init__(self, stream: Union[ActivityStream, dict] = None):
        super(AnnounceEndorsement, self).__init__(stream=stream)