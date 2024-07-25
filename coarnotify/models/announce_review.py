from coarnotify.models.notify import NotifyDocument


class AnnounceReview(NotifyDocument):
    TYPE = ["Announce", "coar-notify:ReviewAction"]
