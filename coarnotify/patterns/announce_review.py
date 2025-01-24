"""
Pattern to represent the Announce Review notification
https://coar-notify.net/specification/1.0.0/announce-review/
"""
from coarnotify.core.notify import NotifyPattern, NotifyTypes, NotifyObject, NotifyItem, NotifyProperties
from coarnotify.core.activitystreams2 import ActivityStreamsTypes, Properties
from coarnotify.exceptions import ValidationError

from typing import Union

__all__ = ["AnnounceReview", "AnnounceReviewContext", "AnnounceReviewItem", "AnnounceReviewObject"]

class AnnounceReview(NotifyPattern):
    """
    Class to represent Announce Review pattern
    """
    TYPE = [ActivityStreamsTypes.ANNOUNCE, NotifyTypes.REVIEW_ACTION]
    """ Announce Review type, including Acitivity Streams Announce and Notify Review Action """

    @property
    def object(self) -> Union["AnnounceReviewObject", None]:
        """
        Custom getter to retrieve Announce Review object

        :return: Announce Review Object
        """
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
    def context(self) -> Union["AnnounceReviewContext", None]:
        """
        Custom getter to retrieve AnnounceReview Context

        :return: AnnounceReviewContext
        """
        c = self.get_property(Properties.CONTEXT)
        if c is not None:
            return AnnounceReviewContext(c,
                                      validate_stream_on_construct=False,
                                      validate_properties=self.validate_properties,
                                      validators=self.validators,
                                      validation_context=Properties.CONTEXT,
                                      properties_by_reference=self._properties_by_reference)
        return None

    def validate(self) -> bool:
        """
        Extends the base validation to make `context` required

        :return: ``True`` if valid, otherwise raises :py:class:`coarnotify.exceptions.ValidationError`
        """
        ve = ValidationError()
        try:
            super(NotifyPattern, self).validate()
        except ValidationError as superve:
            ve = superve

        self.required_and_validate(ve, Properties.CONTEXT, self.context)

        if ve.has_errors():
            raise ve

        return True

class AnnounceReviewContext(NotifyObject):
    """
    Custom Context for Announce Review, specifically to return custom
    Announce Review Item
    """
    @property
    def item(self) -> Union["AnnounceReviewItem", None]:
        """
        Custom getter to retrieve AnnounceReviewItem

        :return: AnnounceReviewItem
        """
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
    """
    Custom AnnounceReviewItem which provides additional validation over the basic NotifyItem
    """

    def validate(self) -> bool:
        """
        In addition to the base validator, this:

        * Reintroduces type validation
        * make ``mediaType`` a required field

        :return: ``True`` if valid, else raises a ValidationError
        """
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
    """
    Custom Announce Review Object to apply custom validation for this pattern
    """

    def validate(self) -> bool:
        """
        In addition to the base validator this:

        * Makes type required

        :return: ``True`` if valid, else raises ValidationError
        """
        ve = ValidationError()
        try:
            super(AnnounceReviewObject, self).validate()
        except ValidationError as superve:
            ve = superve

        self.required_and_validate(ve, Properties.TYPE, self.type)

        if ve.has_errors():
            raise ve

        return True