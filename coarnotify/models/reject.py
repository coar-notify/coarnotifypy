from coarnotify.models.notify import NotifyPattern, NestedPatternObjectMixin, SummaryMixin
from coarnotify.activitystreams2.activitystreams2 import ActivityStreamsTypes, Properties
from coarnotify.exceptions import ValidationError

class Reject(NestedPatternObjectMixin, NotifyPattern, SummaryMixin):
    TYPE = ActivityStreamsTypes.REJECT

    def validate(self):
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
