from coarnotify.models.notify import NotifyDocument, NotifyTypes
from coarnotify.activitystreams2.activitystreams2 import ActivityStreamsTypes

class RequestIngest(NotifyDocument):
    TYPE = [ActivityStreamsTypes.OFFER, NotifyTypes.INGEST_ACTION]
