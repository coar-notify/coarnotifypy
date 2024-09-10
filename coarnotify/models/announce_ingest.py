from coarnotify.models.notify import NotifyDocument, NotifyTypes
from coarnotify.activitystreams2.activitystreams2 import ActivityStreamsTypes

class AnnounceIngest(NotifyDocument):
    TYPE = [ActivityStreamsTypes.ANNOUNCE, NotifyTypes.INGEST_ACTION]
