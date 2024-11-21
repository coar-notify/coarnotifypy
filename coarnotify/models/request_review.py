from coarnotify.models.notify import NotifyPattern, NotifyTypes, NotifyObject, NotifyItem, NotifyProperties
from coarnotify.core.activitystreams2 import ActivityStreamsTypes, Properties
from coarnotify.exceptions import ValidationError

from typing import Union
from copy import deepcopy

class RequestReview(NotifyPattern):
    TYPE = [ActivityStreamsTypes.OFFER, NotifyTypes.REVIEW_ACTION]

    @property
    def object(self) -> Union[NotifyObject, None]:
        o = self.get_property(Properties.OBJECT)
        if o is not None:
            return RequestReviewObject(o,
                                    validate_stream_on_construct=False,
                                    validate_properties=self.validate_properties,
                                    validators=self.validators,
                                    validation_context=Properties.OBJECT,
                                    properties_by_reference=self._properties_by_reference)
        return None


class RequestReviewObject(NotifyObject):
    @property
    def item(self) -> Union[NotifyItem, None]:
        i = self.get_property(NotifyProperties.ITEM)
        if i is not None:
            return RequestReviewItem(i,
                              validate_stream_on_construct=False,
                              validate_properties=self.validate_properties,
                              validators=self.validators,
                              validation_context=NotifyProperties.ITEM,
                              properties_by_reference=self._properties_by_reference)
        return None


class RequestReviewItem(NotifyItem):

    def validate(self):
        # Object does not require `type`, so we override the base validator to just validate
        # the id
        ve = ValidationError()
        try:
            super(RequestReviewItem, self).validate()
        except ValidationError as superve:
            ve = superve

        self.required_and_validate(ve, Properties.TYPE, self.type)
        self.required(ve, NotifyProperties.MEDIA_TYPE, self.media_type)

        if ve.has_errors():
            raise ve
        return True