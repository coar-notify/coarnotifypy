from copy import deepcopy
from coarnotify.test.fixtures import BaseFixtureFactory


class TentativelyRejectFixtureFactory(BaseFixtureFactory):
    @classmethod
    def source(cls, copy=True):
        if copy:
            return deepcopy(TENTATIVELY_REJECT)
        return TENTATIVELY_REJECT

    @classmethod
    def invalid(cls):
        source = cls.source()
        cls._base_invalid(source)
        cls._actor_invalid(source)
        cls._object_invalid(source)
        return source

TENTATIVELY_REJECT = {
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://coar-notify.net"
    ],
    "actor": {
        "id": "https://generic-service-1.com",
        "name": "Generic Service",
        "type": "Service"
    },
    "id": "urn:uuid:b6c7c187-4df2-45c6-8b03-b516b134224b",
    "inReplyTo": "urn:uuid:0370c0fb-bb78-4a9b-87f5-bed307a509dd",
    "object": {
        "actor": {
            "id": "https://orcid.org/0000-0002-1825-0097",
            "name": "Josiah Carberry",
            "type": "Person"
        },
        "id": "urn:uuid:0370c0fb-bb78-4a9b-87f5-bed307a509dd",
        "object": {
            "id": "https://research-organisation.org/repository/preprint/201203/421/",
            "ietf:cite-as": "https://doi.org/10.5555/12345680",
            "ietf:item": {
                "id": "https://research-organisation.org/repository/preprint/201203/421/content.pdf",
                "mediaType": "application/pdf",
                "type": [
                    "Page",
                    "sorg:AboutPage"
                ]
            },
            "type": "sorg:AboutPage"
        },
        "origin": {
            "id": "https://research-organisation.org/repository",
            "inbox": "https://research-organisation.org/inbox/",
            "type": "Service"
        },
        "target": {
            "id": "https://overlay-journal.com/system",
            "inbox": "https://overlay-journal.com/inbox/",
            "type": "Service"
        },
        "type": [
            "Offer",
            "coar-notify:EndorsementAction"
        ]
    },
    "origin": {
        "id": "https://generic-service.com/system",
        "inbox": "https://generic-service.com/system/inbox/",
        "type": "Service"
    },
    "summary": "The offer has been tentatively rejected, subject to further review.",
    "target": {
        "id": "https://some-organisation.org",
        "inbox": "https://some-organisation.org/inbox/",
        "type": "Service"
    },
    "type": "TentativeReject"
}