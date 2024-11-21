from coarnotify.models.notify import NotifyPattern, NotifyTypes, NotifyItem, NotifyProperties, NotifyObject
from coarnotify.core.activitystreams2 import ActivityStreamsTypes, Properties
from coarnotify.exceptions import ValidationError

from typing import Union
from copy import deepcopy

class RequestEndorsement(NotifyPattern):
    TYPE = [ActivityStreamsTypes.OFFER, NotifyTypes.ENDORSMENT_ACTION]

    @property
    def object(self) -> Union[NotifyObject, None]:
        o = self.get_property(Properties.OBJECT)
        if o is not None:
            return RequestEndorsementObject(deepcopy(o),
                                        validate_stream_on_construct=False,
                                        validate_properties=self.validate_properties,
                                        validators=self.validators,
                                        validation_context=Properties.OBJECT)
        return None


class RequestEndorsementObject(NotifyObject):
    @property
    def item(self) -> Union[NotifyItem, None]:
        i = self.get_property(NotifyProperties.ITEM)
        if i is not None:
            return RequestEndorsementItem(deepcopy(i),
                              validate_stream_on_construct=False,
                              validate_properties=self.validate_properties,
                              validators=self.validators,
                              validation_context=NotifyProperties.ITEM)
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
