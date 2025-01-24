"""
Pattern to represent an ``Announce Endorsement`` notification
https://coar-notify.net/specification/1.0.0/announce-endorsement/
"""
from coarnotify.core.notify import NotifyPattern, NotifyTypes, NotifyItem, NotifyProperties, NotifyObject
from coarnotify.core.activitystreams2 import ActivityStreamsTypes, Properties
from coarnotify.exceptions import ValidationError

from typing import Union

__all__ = ["AnnounceEndorsement", "AnnounceEndorsementContext", "AnnounceEndorsementItem"]

class AnnounceEndorsement(NotifyPattern):
    """
    Class to represent an Announce Endorsement pattern
    """
    TYPE = [ActivityStreamsTypes.ANNOUNCE, NotifyTypes.ENDORSMENT_ACTION]
    """Announce Endorsement type, consisting of Activity Streams Announce and Notify Endorsement Action"""

    @property
    def context(self) -> Union["AnnounceEndorsementContext", None]:
        """
        Get a context specific to Announce Endorsement

        :return: The Announce Endorsement context object
        """
        c = self.get_property(Properties.CONTEXT)
        if c is not None:
            return AnnounceEndorsementContext(c,
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


class AnnounceEndorsementContext(NotifyObject):
    """
    Announce Endorsement context object, which extends the base NotifyObject
    to allow us to pass back a custom :py:class:`AnnounceEndorsementItem`
    """
    @property
    def item(self) -> Union["AnnounceEndorsementItem", None]:
        """
        Get a custom :py:class:`AnnounceEndorsementItem`

        :return: the Announce Endorsement Item
        """
        i = self.get_property(NotifyProperties.ITEM)
        if i is not None:
            return AnnounceEndorsementItem(i,
                              validate_stream_on_construct=False,
                              validate_properties=self.validate_properties,
                              validators=self.validators,
                              validation_context=NotifyProperties.ITEM,
                              properties_by_reference=self._properties_by_reference)
        return None


class AnnounceEndorsementItem(NotifyItem):
    """
    Announce Endorsement Item, which extends the base NotifyItem to provide
    additional validation
    """
    def validate(self) -> bool:
        """
        Extends the base validation with validation custom to Announce Endorsement notifications

        * Adds type validation, which the base NotifyItem does not apply
        * Requires the ``mediaType`` value

        :return: ``True`` if valid, otherwise raises a ValidationError
        """
        ve = ValidationError()
        try:
            super(AnnounceEndorsementItem, self).validate()
        except ValidationError as superve:
            ve = superve

        self.required_and_validate(ve, Properties.TYPE, self.type)
        self.required(ve, NotifyProperties.MEDIA_TYPE, self.media_type)

        if ve.has_errors():
            raise ve
        return True