from copy import deepcopy


class RejectFixtureFactory:
    @classmethod
    def source(cls):
        return deepcopy(REJECT)


REJECT = {
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://purl.org/coar/notify"
    ],
    "id": "urn:uuid:668f26e0-2c8d-4117-a0d2-ee713523bcb1",
    "inReplyTo": "urn:uuid:0370c0fb-bb78-4a9b-87f5-bed307a509dd",
    "origin": {
        "id": "https://generic-service.com/system",
        "inbox": "https://generic-service.com/system/inbox/",
        "type": "Service"
    },
    "target": {
        "id": "https://some-organisation.org",
        "inbox": "https://some-organisation.org/inbox/",
        "type": ["Organization", "Service"]
    },
    "type": "Reject",
    # FIXME: this is not part of the spec, added to pass validation checks,
    # awaiting confirmation on the use of object in Reject
    "object": {
        "id": "urn:uuid:4fb3af44-1111-4226-9475-2d09c2d8d9e0",
        "type": "Offer"
    }
}