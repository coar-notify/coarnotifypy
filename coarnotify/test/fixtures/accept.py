from copy import deepcopy


class AcceptFixtureFactory:
    @classmethod
    def source(cls):
        return deepcopy(ACCEPT)


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
    "target": {
        "id": "https://some-organisation.org",
        "inbox": "https://some-organisation.org/inbox/",
        "type": "Organization"
    },
    "type": "Accept"
}