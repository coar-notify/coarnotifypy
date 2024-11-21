from copy import deepcopy
from coarnotify.core.notify import NotifyObject, NotifyService


class NotifyFixtureFactory:
    @classmethod
    def source(cls):
        return deepcopy(BASE_NOTIFY)

    @classmethod
    def target(cls):
        return NotifyService(deepcopy(BASE_NOTIFY["target"]))

    @classmethod
    def origin(cls):
        return NotifyService(deepcopy(BASE_NOTIFY["origin"]))

    @classmethod
    def object(cls):
        return NotifyObject(deepcopy(BASE_NOTIFY["object"]))


BASE_NOTIFY = {
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://purl.org/coar/notify"
    ],
    "id": "urn:uuid:94ecae35-dcfd-4182-8550-22c7164fe23f",
    "type": "Object",
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