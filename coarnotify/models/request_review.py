from coarnotify.models.notify import NotifyDocument


class RequestReview(NotifyDocument):
    TYPE = ["Offer", "coar-notify:ReviewAction"]
