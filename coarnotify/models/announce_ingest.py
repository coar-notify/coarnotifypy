from coarnotify.models.notify import NotifyDocument


class AnnounceIngest(NotifyDocument):
    TYPE = ["Announce", "coar-notify:IngestAction"]
