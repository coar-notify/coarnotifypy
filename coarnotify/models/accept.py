from coarnotify.models.notify import NotifyPattern
from coarnotify.activitystreams2.activitystreams2 import ActivityStreamsTypes, Properties
from coarnotify.exceptions import ValidationError
from coarnotify import validate

class Accept(NotifyPattern):
    TYPE = ActivityStreamsTypes.ACCEPT

    def validate(self):
        ve = ValidationError()
        try:
            super(Accept, self).validate()
        except ValidationError as superve:
            ve = superve

        # Technically, no need to validate the value, as this is handled by the superclass,
        # but leaving it in for completeness
        self.required_and_validate(ve, Properties.IN_REPLY_TO, self.in_reply_to)

        if ve.has_errors():
            raise ve

        return True