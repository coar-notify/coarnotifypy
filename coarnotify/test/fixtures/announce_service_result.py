from copy import deepcopy

from coarnotify.test.fixtures import BaseFixtureFactory


class AnnounceServiceResultFixtureFactory(BaseFixtureFactory):
    @classmethod
    def source(cls, copy=True):
        if copy:
            return deepcopy(ANNOUNCE_SERVICE_RESULT)
        return ANNOUNCE_SERVICE_RESULT

    @classmethod
    def invalid(cls):
        source = cls.source()
        cls._base_invalid(source)
        cls._actor_invalid(source)
        cls._object_invalid(source)
        cls._context_invalid(source)
        return source

ANNOUNCE_SERVICE_RESULT = {
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://coar-notify.net"
    ],
    "actor": {
        "id": "https://overlay-journal.com",
        "name": "Overlay Journal",
        "type": "Service"
    },
    "context": {
        "id": "https://research-organisation.org/repository/preprint/201203/421/"
    },
    "id": "urn:uuid:94ecae35-dcfd-4182-8550-22c7164fe23f",
    "inReplyTo": "urn:uuid:0370c0fb-bb78-4a9b-87f5-bed307a509dd",
    "object": {
        "id": "https://overlay-journal.com/information-page",
        "type": [
            "Page",
            "sorg:WebPage"
        ]
    },
    "origin": {
        "id": "https://overlay-journal.com/system",
        "inbox": "https://overlay-journal.com/inbox/",
        "type": "Service"
    },
    "target": {
        "id": "https://generic-service.com/system",
        "inbox": "https://generic-service.com/system/inbox/",
        "type": "Service"
    },
    "type": [
        "Announce"
    ]
}