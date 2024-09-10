from coarnotify.models.notify import NotifyDocument
from coarnotify.activitystreams2.activitystreams2 import ActivityStreamsTypes

class Reject(NotifyDocument):
    TYPE = ActivityStreamsTypes.REJECT
