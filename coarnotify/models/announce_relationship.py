from coarnotify.models.notify import NotifyDocument, NotifyTypes
from coarnotify.activitystreams2.activitystreams2 import ActivityStreamsTypes


class AnnounceRelationship(NotifyDocument):
    TYPE = [ActivityStreamsTypes.ANNOUNCE, NotifyTypes.RELATIONSHIP_ACTION]
