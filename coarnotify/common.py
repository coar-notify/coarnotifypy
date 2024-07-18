from typing import List
from coarnotify.activitystreams2.activitystreams2 import ActivityStream, Properties
from coarnotify.models import (
    Accept,
    AnnounceEndorsement,
    AnnounceIngest,
    AnnounceRelationship,
    AnnounceReview
)
from coarnotify.exceptions import NotifyException


class COARNotifyFactory:

    MODELS = [
        Accept,
        AnnounceEndorsement,
        AnnounceIngest,
        AnnounceRelationship,
        AnnounceReview
    ]

    @classmethod
    def get_by_types(cls, incoming_types:List[str]):
        for m in cls.MODELS:
            document_types = m.TYPE
            if not isinstance(document_types, list):
                document_types = [document_types]
            if not isinstance(incoming_types, list):
                incoming_types = [incoming_types]
            if set(document_types).issubset(set(incoming_types)):
                return m
        return None

    @classmethod
    def get_by_object(cls, data):
        stream = ActivityStream(data)

        types = stream.get_property(Properties.TYPE)
        if types is None:
            raise NotifyException("No type found in object")

        klazz = cls.get_by_types(types)

        inst = klazz(data)
        return inst

