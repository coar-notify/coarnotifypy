from coarnotify.models.notify import NotifyPattern, NestedPatternObjectMixin, SummaryMixin, NotifyTypes
from coarnotify.activitystreams2.activitystreams2 import ActivityStreamsTypes, Properties
from coarnotify.exceptions import ValidationError

class UnprocessableNotification(NotifyPattern, SummaryMixin):
    TYPE = [ActivityStreamsTypes.FLAG, NotifyTypes.UNPROCESSABLE_NOTIFICATION]

    def validate(self):
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
