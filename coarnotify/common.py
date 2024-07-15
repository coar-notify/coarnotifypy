from typing import List
from coarnotify.activitystreams.activitystreams import ActivityStream
from coarnotify.models import Accept, AnnounceEndorsement, AnnounceIngest, AnnounceRelationship
from coarnotify.exceptions import NotifyException


class COARNotifyFactory:

    MODELS = [
        Accept,
        AnnounceEndorsement,
        AnnounceIngest,
        AnnounceRelationship
    ]

    @classmethod
    def get_by_types(cls, incoming_types:List[str]):
        for m in cls.MODELS:
            idents = m.IDENTIFY_BY_TYPE
            for ident_set in idents:
                match = [True if x in incoming_types else False for x in ident_set]
                if all(match):
                    return m
        return None

        # for entry_point in iter_entry_points(group='coarnotify'):
        #     if entry_point.name == type:
        #         return entry_point.load()()
        # return None

    @classmethod
    def get_by_object(cls, data):
        stream = ActivityStream(data)

        types = stream.type
        if types is None:
            raise NotifyException("No type found in object")

        klazz = cls.get_by_types(types)

        inst = klazz(data)
        return inst

