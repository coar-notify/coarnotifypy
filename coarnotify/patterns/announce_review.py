from coarnotify.core.notify import NotifyPattern, NotifyTypes, NotifyObject, NotifyItem, NotifyProperties
from coarnotify.core.activitystreams2 import ActivityStreamsTypes, Properties
from coarnotify.exceptions import ValidationError

from typing import Union


class AnnounceReview(NotifyPattern):
    TYPE = [ActivityStreamsTypes.ANNOUNCE, NotifyTypes.REVIEW_ACTION]

    @property
    def object(self) -> Union[NotifyObject, None]:
        o = self.get_property(Properties.OBJECT)
        if o is not None:
            return AnnounceReviewObject(o,
                                validate_stream_on_construct=False,
                                validate_properties=self.validate_properties,
                                validators=self.validators,
                                validation_context=Properties.OBJECT,
                                properties_by_reference=self._properties_by_reference)
        return None

    @property
    def context(self) -> Union[NotifyObject, None]:
        c = self.get_property(Properties.CONTEXT)
        if c is not None:
            return AnnounceReviewContext(c,
                                      validate_stream_on_construct=False,
                                      validate_properties=self.validate_properties,
                                      validators=self.validators,
                                      validation_context=Properties.CONTEXT,
                                      properties_by_reference=self._properties_by_reference)
        return None

class AnnounceReviewContext(NotifyObject):
    @property
    def item(self) -> Union[NotifyItem, None]:
        i = self.get_property(NotifyProperties.ITEM)
        if i is not None:
            return AnnounceReviewItem(i,
                              validate_stream_on_construct=False,
                              validate_properties=self.validate_properties,
                              validators=self.validators,
                              validation_context=NotifyProperties.ITEM,
                              properties_by_reference=self._properties_by_reference)
        return None


class AnnounceReviewItem(NotifyItem):
    def validate(self):
        # Object does not require `type`, so we override the base validator to just validate
        # the id
        ve = ValidationError()
        try:
            super(AnnounceReviewItem, self).validate()
        except ValidationError as superve:
            ve = superve

        self.required_and_validate(ve, Properties.TYPE, self.type)
        self.required(ve, NotifyProperties.MEDIA_TYPE, self.media_type)

        if ve.has_errors():
            raise ve
        return True


class AnnounceReviewObject(NotifyObject):
    def validate(self):
        ve = ValidationError()
        try:
            super(AnnounceReviewObject, self).validate()
        except ValidationError as superve:
            ve = superve

        self.required_and_validate(ve, Properties.TYPE, self.type)

        if ve.has_errors():
            raise ve

        return True