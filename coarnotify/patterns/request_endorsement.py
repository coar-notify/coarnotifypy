"""
Pattern to represent a Request Endorsement notification
https://coar-notify.net/specification/1.0.0/request-endorsement/
"""
from coarnotify.core.notify import NotifyPattern, NotifyTypes, NotifyItem, NotifyProperties, NotifyObject
from coarnotify.core.activitystreams2 import ActivityStreamsTypes, Properties
from coarnotify.exceptions import ValidationError

from typing import Union

__all__ = ["RequestEndorsement", "RequestEndorsementObject", "RequestEndorsementItem"]

class RequestEndorsement(NotifyPattern):
    """
    Class to represent a Request Endorsement notification
    """
    TYPE = [ActivityStreamsTypes.OFFER, NotifyTypes.ENDORSMENT_ACTION]
    """Request Endorsement types, including an ActivityStreams offer and a COAR Notify Endorsement Action"""

    @property
    def object(self) -> Union["RequestEndorsementObject", None]:
        """
        Custom getter to retrieve the object property as a RequestEndorsementObject

        :return:
        """
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
    """
    Custom object class for Request Endorsement to provide the custom item getter
    """

    @property
    def item(self) -> Union["RequestEndorsementItem", None]:
        """
        Custom getter to retrieve the item property as a RequestEndorsementItem
        :return:
        """
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
    """
    Custom item class for Request Endorsement to provide the custom validation
    """

    def validate(self) -> bool:
        """
        Extend the base validation to include the following constraints:

        * The item type is required and must validate
        * The ``mediaType`` property is required

        :return: ``True`` if validation passes, otherwise raise a ``ValidationError``
        """
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
