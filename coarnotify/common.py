#from pkg_resources import iter_entry_points
from typing import List
from activitystreams.activitystreams import ActivityStream
from coarnotify.models.announce_endorsement import AnnounceEndorsement
from coarnotify.exceptions import NotifyException

class COARNotifyFactory:

    MODELS = [
        AnnounceEndorsement
    ]

    @classmethod
    def get_by_types(cls, type:List[str]):
        for m in cls.MODELS:
            types = m.TYPE
            if not isinstance(types, list):
                types = [types]
            if set(types) == set(type):
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

