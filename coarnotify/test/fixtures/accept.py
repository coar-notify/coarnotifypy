from copy import deepcopy
from coarnotify.test.fixtures import BaseFixtureFactory


class AcceptFixtureFactory(BaseFixtureFactory):
    @classmethod
    def source(cls):
        return deepcopy(ACCEPT)

    @classmethod
    def invalid(cls):
        source = cls.source()
        cls._base_invalid(source)
        return source


ACCEPT = {
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://purl.org/coar/notify"
    ],
    "id": "urn:uuid:4fb3af44-d4f8-4226-9475-2d09c2d8d9e0",
    "inReplyTo": "urn:uuid:0370c0fb-bb78-4a9b-87f5-bed307a509dd",
    "origin": {
        "id": "https://generic-service.com/system",
        "inbox": "https://generic-service.com/system/inbox/",
        "type": "Service"
    },
    # FIXME: this is not part of the spec, added to pass validation checks,
    # awaiting confirmation on the use of object in Reject
    "object": {
        "id": "urn:uuid:4fb3af44-1111-4226-9475-2d09c2d8d9e0",
        "type": "sorg:AboutPage"
    },
    "target": {
        "id": "https://some-organisation.org",
        "inbox": "https://some-organisation.org/inbox/",
        "type": ["Organization", "Service"]
    },
    "type": "Accept"
}