
from coarnotify.models.notify import NotifyPattern, NotifyObject
from coarnotify.activitystreams2.activitystreams2 import ActivityStreamsTypes, Properties
from coarnotify.exceptions import ValidationError
from typing import Union
from copy import deepcopy

class TentativelyAccept(NotifyPattern):
    TYPE = ActivityStreamsTypes.TENTATIVE_ACCEPT

    @property
    def summary(self) -> str:
        return self.get_property(Properties.SUMMARY)

    @summary.setter
    def summary(self, summary: str):
        self.set_property(Properties.SUMMARY, summary)

    @property
    def object(self) -> Union[NotifyPattern, NotifyObject, None]:
        o = self.get_property(Properties.OBJECT)
        if o is not None:
            from coarnotify.common import COARNotifyFactory     # late import to avoid circular dependency
            nested = COARNotifyFactory.get_by_object(deepcopy(o),
                                    validate_stream_on_construct=False,
                                    validate_properties=self.validate_properties,
                                    validators=self.validators,
                                    validation_context=None)    # don't supply a validation context, as these objects are not typical nested objects
            if nested is not None:
                return nested

            # if we are unable to construct the typed nested object, just return a generic object
            return NotifyObject(deepcopy(o),
                             validate_stream_on_construct=False,
                             validate_properties=self.validate_properties,
                             validators=self.validators,
                             validation_context=Properties.OBJECT)
        return None

    @object.setter
    def object(self, value: Union[NotifyObject, NotifyPattern]):
        self.set_property(Properties.OBJECT, value.doc)

    def validate(self):
        ve = ValidationError()
        try:
            super(TentativelyAccept, self).validate()
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