from copy import deepcopy
from coarnotify.test.fixtures import BaseFixtureFactory


class AnnounceEndorsementFixtureFactory(BaseFixtureFactory):
    @classmethod
    def source(cls):
        return deepcopy(ANNOUNCE_ENDORSEMENT)

    @classmethod
    def invalid(cls):
        source = cls.source()

        cls._base_invalid(source)
        cls._actor_invalid(source)
        cls._object_invalid(source)
        cls._context_invalid(source)

        return source


ANNOUNCE_ENDORSEMENT = {
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://purl.org/coar/notify"
    ],
    "id": "urn:uuid:94ecae35-dcfd-4182-8550-22c7164fe23f",
    "type": [
        "Announce",
        "coar-notify:EndorsementAction"
    ],
    "origin": {
        "id": "https://overlay-journal.com/system",
        "inbox": "https://overlay-journal.com/inbox/",
        "type": "Service"
    },
    "object": {
        "id": "https://overlay-journal.com/articles/00001/",
        "ietf:cite-as": "https://overlay-journal.com/articles/00001/",
        "type": [
            "Page",
            "sorg:WebPage"
        ]
    },
    "target": {
        "id": "https://research-organisation.org/repository",
        "inbox": "https://research-organisation.org/inbox/",
        "type": "Service"
    },
    "actor": {
        "id": "https://overlay-journal.com",
        "name": "Overlay Journal",
        "type": "Service"
    },
    "inReplyTo": "urn:uuid:0370c0fb-bb78-4a9b-87f5-bed307a509dd",
    "context": {
        "id": "https://research-organisation.org/repository/preprint/201203/421/",
        "ietf:cite-as": "https://doi.org/10.5555/12345680",
        "ietf:item": {
            "id": "https://research-organisation.org/repository/preprint/201203/421/content.pdf",
            "mediaType": "application/pdf",
            "type": [
                "Article",
                "sorg:ScholarlyArticle"
            ]
        },
        "type": "sorg:AboutPage"
    }
}