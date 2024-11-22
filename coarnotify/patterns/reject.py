"""
Pattern to represent a Reject notification
https://coar-notify.net/specification/1.0.0/reject/
"""

from coarnotify.core.notify import NotifyPattern, NestedPatternObjectMixin, SummaryMixin
from coarnotify.core.activitystreams2 import ActivityStreamsTypes, Properties
from coarnotify.exceptions import ValidationError

__all__ = ["Reject"]

class Reject(NestedPatternObjectMixin, NotifyPattern, SummaryMixin):
    """
    Class to represent a Reject notification
    """

    TYPE = ActivityStreamsTypes.REJECT
    """Reject type, the ActivityStreams Reject type"""

    def validate(self) -> bool:
        """
        In addition to the base validation apply the following constraints:

        * The ``inReplyTo`` property is required
        * The ``inReplyTo`` value must match the ``object.id`` value

        :return: ``True`` if the validation passes, otherwise raise a ``ValidationError``
        """
        ve = ValidationError()
        try:
            super(Reject, self).validate()
        except ValidationError as superve:
            ve = superve

        # Technically, no need to validate the value, as this is handled by the superclass,
        # but leaving it in for completeness
        self.required_and_validate(ve, Properties.IN_REPLY_TO, self.in_reply_to)

        objid = self.object.id if self.object else None
        if self.in_reply_to != objid:
            ve.add_error(Properties.IN_REPLY_TO, f"Expected inReplyTo id to be the same as the nested object id. inReplyTo: {self.in_reply_to}, object.id: {objid}")

        if ve.has_errors():
            raise ve

        return True
