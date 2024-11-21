from coarnotify.models.notify import NotifyPattern, NotifyTypes, NotifyObject
from coarnotify.core.activitystreams2 import ActivityStreamsTypes, Properties
from coarnotify.exceptions import ValidationError

from typing import Union
from copy import deepcopy

class AnnounceRelationship(NotifyPattern):
    TYPE = [ActivityStreamsTypes.ANNOUNCE, NotifyTypes.RELATIONSHIP_ACTION]

    @property
    def object(self) -> Union[NotifyObject, None]:
        o = self.get_property(Properties.OBJECT)
        if o is not None:
            return AnnounceRelationshipObject(o,
                                validate_stream_on_construct=False,
                                validate_properties=self.validate_properties,
                                validators=self.validators,
                                validation_context=Properties.OBJECT,
                                properties_by_reference=self._properties_by_reference)
        return None


class AnnounceRelationshipObject(NotifyObject):
    def validate(self):
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
