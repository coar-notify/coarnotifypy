from coarnotify.models.notify import NotifyDocument, NotifyTypes
from coarnotify.activitystreams2.activitystreams2 import ActivityStreamsTypes

class AnnounceReview(NotifyDocument):
    TYPE = [ActivityStreamsTypes.ANNOUNCE, NotifyTypes.REVIEW_ACTION]
