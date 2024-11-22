"""
Pattern to represent a Request Review notification
https://coar-notify.net/specification/1.0.0/request-review/
"""
from coarnotify.core.notify import NotifyPattern, NotifyTypes, NotifyObject, NotifyItem, NotifyProperties
from coarnotify.core.activitystreams2 import ActivityStreamsTypes, Properties
from coarnotify.exceptions import ValidationError

from typing import Union

__all__ = ["RequestReview", "RequestReviewObject", "RequestReviewItem"]

class RequestReview(NotifyPattern):
    """
    Class to represent a Request Review notification
    """

    TYPE = [ActivityStreamsTypes.OFFER, NotifyTypes.REVIEW_ACTION]
    """Request Review types, including an ActivityStreams offer and a COAR Notify Review Action"""

    @property
    def object(self) -> Union["RequestReviewObject", None]:
        """
        Custom getter to retrieve the object property as a RequestReviewObject
        :return:
        """
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
    """
    Custom Request Review Object class to return the custom RequestReviewItem class
    """
    @property
    def item(self) -> Union["RequestReviewItem", None]:
        """
        Custom getter to retrieve the item property as a RequestReviewItem
        :return:
        """
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
    """
    Custom Request Review Item class to provide the custom validation
    """

    def validate(self) -> bool:
        """
        Extend the base validation to include the following constraints:

        * The type property is required and must validate
        * the ``mediaType`` property is required

        :return: ``True`` if validation passes, else raise a ``ValidationError``
        """
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