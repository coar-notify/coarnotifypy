"""
Pattern to represent the Announce Service Result notification
https://coar-notify.net/specification/1.0.0/announce-resource/
"""
from coarnotify.core.notify import NotifyPattern, NotifyItem, NotifyProperties, NotifyObject
from coarnotify.core.activitystreams2 import ActivityStreamsTypes, Properties
from coarnotify.exceptions import ValidationError

from typing import Union

__all__ = ["AnnounceServiceResult", "AnnounceServiceResultObject", "AnnounceServiceResultContext", "AnnounceServiceResultItem"]

class AnnounceServiceResult(NotifyPattern):
    """
    Class to represent the Announce Service Result Pattern
    """

    TYPE = ActivityStreamsTypes.ANNOUNCE
    """Announce Service Result type, the ActivityStreams Announce type"""

    @property
    def object(self) -> Union["AnnounceServiceResultObject", None]:
        """
        Custom getter to retrieve the object property as an AnnounceServiceResultObject

        :return: AnnounceServiceResultObject
        """
        o = self.get_property(Properties.OBJECT)
        if o is not None:
            return AnnounceServiceResultObject(o,
                                        validate_stream_on_construct=False,
                                        validate_properties=self.validate_properties,
                                        validators=self.validators,
                                        validation_context=Properties.OBJECT,
                                        properties_by_reference=self._properties_by_reference)
        return None

    @property
    def context(self) -> Union["AnnounceServiceResultContext", None]:
        """
        Custom getter to retrieve the context property as an AnnounceServiceResultContext

        :return:    AnnounceSericeResultCOntext
        """
        c = self.get_property(Properties.CONTEXT)
        if c is not None:
            return AnnounceServiceResultContext(c,
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


class AnnounceServiceResultContext(NotifyObject):
    """
    Custom object class for Announce Service Result to provide the custom item getter
    """

    @property
    def item(self) -> Union["AnnounceServiceResultItem", None]:
        """
        Custom getter to retrieve the item property as an AnnounceServiceResultItem
        :return:
        """
        i = self.get_property(NotifyProperties.ITEM)
        if i is not None:
            return AnnounceServiceResultItem(i,
                              validate_stream_on_construct=False,
                              validate_properties=self.validate_properties,
                              validators=self.validators,
                              validation_context=NotifyProperties.ITEM,
                              properties_by_reference=self._properties_by_reference)
        return None

class AnnounceServiceResultItem(NotifyItem):
    """
    Custom item class for Announce Service Result to apply the custom validation
    """

    def validate(self) -> bool:
        """
        Beyond the base validation, apply the following:

        * Make type required and avlid
        * Make the ``mediaType`` required

        :return: ``True`` if validation passes, else raise a ``ValidationError``
        """
        ve = ValidationError()
        try:
            super(AnnounceServiceResultItem, self).validate()
        except ValidationError as superve:
            ve = superve

        self.required_and_validate(ve, Properties.TYPE, self.type)
        self.required(ve, NotifyProperties.MEDIA_TYPE, self.media_type)

        if ve.has_errors():
            raise ve
        return True

class AnnounceServiceResultObject(NotifyObject):
    """
    Custom object class for Announce Service Result to apply the custom validation
    """

    def validate(self) -> bool:
        """
        Extend the base validation to include the following constraints:

        * The object type is required and must validate

        :return: ``True`` if validation passes, else raise a ``ValidationError``
        """
        ve = ValidationError()
        try:
            super(AnnounceServiceResultObject, self).validate()
        except ValidationError as superve:
            ve = superve

        self.required_and_validate(ve, Properties.TYPE, self.type)

        if ve.has_errors():
            raise ve

        return True