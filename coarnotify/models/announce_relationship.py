from coarnotify.models.notify import NotifyDocument


class AnnounceRelationship(NotifyDocument):
    TYPE = ["Announce", "coar-notify:RelationshipAction"]
