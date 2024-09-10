from coarnotify.models.notify import NotifyDocument, NotifyTypes
from coarnotify.activitystreams2.activitystreams2 import ActivityStreamsTypes

class AnnounceEndorsement(NotifyDocument):
    TYPE = [ActivityStreamsTypes.ANNOUNCE, NotifyTypes.ENDORSMENT_ACTION]
