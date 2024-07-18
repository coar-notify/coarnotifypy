from typing import Union

from coarnotify.models.notify import NotifyDocument
from coarnotify.activitystreams2.activitystreams2 import ActivityStream


class AnnounceRelationship(NotifyDocument):
    TYPE = ["Announce", "coar-notify:RelationshipAction"]

    def __init__(self, stream: Union[ActivityStream, dict] = None):
        super(AnnounceRelationship, self).__init__(stream=stream)