from typing import Union

from coarnotify.models.notify import Notify
from coarnotify.activitystreams.activitystreams import ActivityStream


class AnnounceEndorsement(Notify):
    DEFAULT_TYPE = ["Announce", "coar-notify:EndorsementAction"]
    ALLOWED_TYPES = DEFAULT_TYPE
    FORCE_TYPE = True

    def __init__(self, stream: Union[ActivityStream, dict] = None):
        super(AnnounceEndorsement, self).__init__(stream=stream)