from coarnotify.models.notify import NotifyDocument


class RequestIngest(NotifyDocument):
    TYPE = ["Offer", "coar-notify:IngestAction"]
