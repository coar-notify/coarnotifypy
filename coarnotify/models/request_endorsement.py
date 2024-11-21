from coarnotify.core.notify import NotifyPattern, NotifyTypes, NotifyItem, NotifyProperties, NotifyObject
from coarnotify.core.activitystreams2 import ActivityStreamsTypes, Properties
from coarnotify.exceptions import ValidationError

from typing import Union


class RequestEndorsement(NotifyPattern):
    TYPE = [ActivityStreamsTypes.OFFER, NotifyTypes.ENDORSMENT_ACTION]

    @property
    def object(self) -> Union[NotifyObject, None]:
        o = self.get_property(Properties.OBJECT)
        if o is not None:
            return RequestEndorsementObject(o,
                                        validate_stream_on_construct=False,
                                        validate_properties=self.validate_properties,
                                        validators=self.validators,
                                        validation_context=Properties.OBJECT,
                                        properties_by_reference=self._properties_by_reference)
        return None


class RequestEndorsementObject(NotifyObject):
    @property
    def item(self) -> Union[NotifyItem, None]:
        i = self.get_property(NotifyProperties.ITEM)
        if i is not None:
            return RequestEndorsementItem(i,
                              validate_stream_on_construct=False,
                              validate_properties=self.validate_properties,
                              validators=self.validators,
                              validation_context=NotifyProperties.ITEM,
                              properties_by_reference=self._properties_by_reference)
        return None


class RequestEndorsementItem(NotifyItem):

    def validate(self):
        # Object does not require `type`, so we override the base validator to just validate
        # the id
        ve = ValidationError()
        try:
            super(RequestEndorsementItem, self).validate()
        except ValidationError as superve:
            ve = superve

        self.required_and_validate(ve, Properties.TYPE, self.type)
        self.required(ve, NotifyProperties.MEDIA_TYPE, self.media_type)

        if ve.has_errors():
            raise ve
        return True
