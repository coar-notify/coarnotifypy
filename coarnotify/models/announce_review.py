from coarnotify.models.notify import NotifyPattern, NotifyTypes, NotifyObject, NotifyItem, NotifyProperties
from coarnotify.activitystreams2.activitystreams2 import ActivityStreamsTypes, Properties
from coarnotify.exceptions import ValidationError

from typing import Union
from copy import deepcopy

class AnnounceReview(NotifyPattern):
    TYPE = [ActivityStreamsTypes.ANNOUNCE, NotifyTypes.REVIEW_ACTION]

    @property
    def object(self) -> Union[NotifyObject, None]:
        o = self.get_property(Properties.OBJECT)
        if o is not None:
            return AnnounceReviewObject(deepcopy(o),
                                validate_stream_on_construct=False,
                                validate_properties=self.validate_properties,
                                validators=self.validators,
                                validation_context=Properties.OBJECT)
        return None

    @property
    def context(self) -> Union[NotifyObject, None]:
        c = self.get_property(Properties.CONTEXT)
        if c is not None:
            return AnnounceReviewContext(deepcopy(c),
                                              validate_stream_on_construct=False,
                                              validate_properties=self.validate_properties,
                                              validators=self.validators,
                                              validation_context=Properties.CONTEXT)
        return None

class AnnounceReviewContext(NotifyObject):
    @property
    def item(self) -> Union[NotifyItem, None]:
        i = self.get_property(NotifyProperties.ITEM)
        if i is not None:
            return AnnounceReviewItem(deepcopy(i),
                              validate_stream_on_construct=False,
                              validate_properties=self.validate_properties,
                              validators=self.validators,
                              validation_context=NotifyProperties.ITEM)
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