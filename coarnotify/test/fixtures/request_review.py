from copy import deepcopy
from coarnotify.test.fixtures import BaseFixtureFactory


class RequestReviewFixtureFactory(BaseFixtureFactory):
    @classmethod
    def source(cls, copy=True):
        if copy:
            return deepcopy(REQUEST_REVIEW)
        return REQUEST_REVIEW

    @classmethod
    def invalid(cls):
        source = cls.source()
        cls._base_invalid(source)
        cls._actor_invalid(source)
        cls._object_invalid(source)
        return source


REQUEST_REVIEW = {
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://coar-notify.net"
    ],
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
                "Article",
                "sorg:ScholarlyArticle"
            ]
        },
        "type": [
            "Page",
            "sorg:AboutPage"
        ]
    },
    "origin": {
        "id": "https://research-organisation.org/repository",
        "inbox": "https://research-organisation.org/inbox/",
        "type": "Service"
    },
    "target": {
        "id": "https://review-service.com/system",
        "inbox": "https://review-service.com/inbox/",
        "type": "Service"
    },
    "type": [
        "Offer",
        "coar-notify:ReviewAction"
    ]
}