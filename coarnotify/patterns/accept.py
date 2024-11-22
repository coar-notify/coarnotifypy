"""
Pattern to represent an Accept notification
https://coar-notify.net/specification/1.0.0/accept/
"""
from coarnotify.core.notify import NotifyPattern, NestedPatternObjectMixin
from coarnotify.core.activitystreams2 import ActivityStreamsTypes, Properties
from coarnotify.exceptions import ValidationError

__all__ = ["Accept"]

class Accept(NestedPatternObjectMixin, NotifyPattern):
    """
    Class to represent an Accept notification
    """
    TYPE = ActivityStreamsTypes.ACCEPT
    """ The Accept type """

    def validate(self) -> bool:
        """
        Validate the Accept pattern.

        In addition to the base validation, this:

        * Makes ``inReplyTo`` required
        * Requires the ``inReplyTo`` value to be the same as the ``object.id`` value

        :return: ``True`` if valid, otherwise raises a :py:class:`coarnotify.exceptions.ValidationError`
        """
        ve = ValidationError()
        try:
            super(Accept, self).validate()
        except ValidationError as superve:
            ve = superve

        # Technically, no need to validate the value, as this is handled by the superclass,
        # but leaving it in for completeness
        self.required_and_validate(ve, Properties.IN_REPLY_TO, self.in_reply_to)

        objid = self.object.id if self.object else None
        if self.in_reply_to != objid:
            ve.add_error(Properties.IN_REPLY_TO,
                         f"Expected inReplyTo id to be the same as the nested object id. inReplyTo: {self.in_reply_to}, object.id: {objid}")

        if ve.has_errors():
            raise ve

        return True