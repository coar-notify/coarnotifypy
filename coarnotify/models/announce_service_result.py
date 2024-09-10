from coarnotify.models.notify import NotifyDocument
from coarnotify.activitystreams2.activitystreams2 import ActivityStreamsTypes

class AnnounceServiceResult(NotifyDocument):
    TYPE = ActivityStreamsTypes.ANNOUNCE
