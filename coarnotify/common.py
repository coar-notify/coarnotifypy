from typing import List
from coarnotify.activitystreams2.activitystreams2 import ActivityStream, Properties
from coarnotify.models import (
    Accept,
    AnnounceEndorsement,
    AnnounceIngest,
    AnnounceRelationship,
    AnnounceReview,
    AnnounceServiceResult,
    Reject,
    RequestEndorsement
)
from coarnotify.exceptions import NotifyException


class COARNotifyFactory:

    MODELS = [
        Accept,
        AnnounceEndorsement,
        AnnounceIngest,
        AnnounceRelationship,
        AnnounceReview,
        AnnounceServiceResult,
        Reject,
        RequestEndorsement
    ]

    @classmethod
    def get_by_types(cls, incoming_types:List[str]):
        if not isinstance(incoming_types, list):
            incoming_types = [incoming_types]

        candidate = None
        candidate_fit = None

        for m in cls.MODELS:
            document_types = m.TYPE
            if not isinstance(document_types, list):
                document_types = [document_types]
            if set(document_types).issubset(set(incoming_types)):
                if candidate_fit is None:
                    candidate = m
                    candidate_fit = len(incoming_types) - len(document_types)
                    if candidate_fit == 0:
                        return candidate

                else:
                    fit = len(incoming_types) - len(document_types)
                    if fit == 0:
                        return m
                    if abs(fit) < abs(candidate_fit):
                        candidate = m
                        candidate_fit = fit

        return candidate

    @classmethod
    def get_by_object(cls, data):
        stream = ActivityStream(data)

        types = stream.get_property(Properties.TYPE)
        if types is None:
            raise NotifyException("No type found in object")

        klazz = cls.get_by_types(types)

        inst = klazz(data)
        return inst

