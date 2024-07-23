from coarnotify.models.notify import NotifyDocument


class RequestEndorsement(NotifyDocument):
    TYPE = ["Offer", "coar-notify:EndorsementAction"]
