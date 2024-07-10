from typing import Union

from coarnotify.models.notify import Notify
from coarnotify.activitystreams.activitystreams import ActivityStream


class Accept(Notify):
    DEFAULT_TYPE = "Accept"
    ALLOWED_TYPES = [DEFAULT_TYPE]
    FORCE_TYPE = True

    def __init__(self, stream: Union[ActivityStream, dict] = None):
        super(Accept, self).__init__(stream=stream)

