from coarnotify.models.notify import NotifyDocument, NotifyTypes
from coarnotify.activitystreams2.activitystreams2 import ActivityStreamsTypes

class RequestEndorsement(NotifyDocument):
    TYPE = [ActivityStreamsTypes.OFFER, NotifyTypes.ENDORSMENT_ACTION]
