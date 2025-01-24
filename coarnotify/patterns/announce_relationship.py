"""
Pattern to represent an Announce Relationship notification
https://coar-notify.net/specification/1.0.0/announce-relationship/
"""
from coarnotify.core.notify import NotifyPattern, NotifyTypes, NotifyObject
from coarnotify.core.activitystreams2 import ActivityStreamsTypes, Properties
from coarnotify.exceptions import ValidationError

from typing import Union

__all__ = ["AnnounceRelationship", "AnnounceRelationshipObject"]

class AnnounceRelationship(NotifyPattern):
    """
    Class to represent an Announce Relationship notification
    """
    TYPE = [ActivityStreamsTypes.ANNOUNCE, NotifyTypes.RELATIONSHIP_ACTION]
    """Announce Relationship types, including an ActivityStreams announce and a COAR Notify Relationship Action"""

    @property
    def object(self) -> Union["AnnounceRelationshipObject", None]:
        """Custom getter to retrieve the object property as an AnnounceRelationshipObject"""
        o = self.get_property(Properties.OBJECT)
        if o is not None:
            return AnnounceRelationshipObject(o,
                                validate_stream_on_construct=False,
                                validate_properties=self.validate_properties,
                                validators=self.validators,
                                validation_context=Properties.OBJECT,
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


class AnnounceRelationshipObject(NotifyObject):
    """
    Custom object class for Announce Relationship to apply the custom validation
    """
    def validate(self) -> bool:
        """
        Extend the base validation to include the following constraints:

        * The object triple is required and each part must validate

        :return:
        """
        ve = ValidationError()
        try:
            super(AnnounceRelationshipObject, self).validate()
        except ValidationError as superve:
            ve = superve

        self.required_and_validate(ve, Properties.TYPE, self.type)

        subject, relationship, object = self.triple
        self.required_and_validate(ve, Properties.SUBJECT_TRIPLE, subject)
        self.required_and_validate(ve, Properties.RELATIONSHIP_TRIPLE, relationship)
        self.required_and_validate(ve, Properties.OBJECT_TRIPLE, object)

        if ve.has_errors():
            raise ve

        return True
