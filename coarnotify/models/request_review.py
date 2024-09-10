from coarnotify.models.notify import NotifyDocument, NotifyTypes
from coarnotify.activitystreams2.activitystreams2 import ActivityStreamsTypes

class RequestReview(NotifyDocument):
    TYPE = [ActivityStreamsTypes.OFFER, NotifyTypes.REVIEW_ACTION]
