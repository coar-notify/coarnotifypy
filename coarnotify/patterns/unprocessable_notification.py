"""
Pattern to represent the Unprocessable Notification notification
https://coar-notify.net/specification/1.0.0/unprocessable/
"""

from coarnotify.core.notify import NotifyPattern, SummaryMixin, NotifyTypes
from coarnotify.core.activitystreams2 import ActivityStreamsTypes, Properties
from coarnotify.exceptions import ValidationError

__all__ = ["UnprocessableNotification"]

class UnprocessableNotification(NotifyPattern, SummaryMixin):
    """
    Class to represent the Unprocessable Notification notification
    """
    TYPE = [ActivityStreamsTypes.FLAG, NotifyTypes.UNPROCESSABLE_NOTIFICATION]
    """Unprocessable Notification types, including an ActivityStreams Flag and a COAR Notify Unprocessable Notification"""

    def validate(self) -> bool:
        """
        In addition to the base validation apply the following constraints:

        * The ``inReplyTo`` property is required
        * The ``summary`` property is required

        :return:
        """
        ve = ValidationError()
        try:
            super(UnprocessableNotification, self).validate()
        except ValidationError as superve:
            ve = superve

        # Technically, no need to validate the value, as this is handled by the superclass,
        # but leaving it in for completeness
        self.required_and_validate(ve, Properties.IN_REPLY_TO, self.in_reply_to)
        self.required(ve, Properties.SUMMARY, self.summary)

        if ve.has_errors():
            raise ve

        return True
