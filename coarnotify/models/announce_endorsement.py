from coarnotify.models.notify import NotifyDocument


class AnnounceEndorsement(NotifyDocument):
    TYPE = ["Announce", "coar-notify:EndorsementAction"]
