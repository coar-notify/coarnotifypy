from unittest import TestCase

from coarnotify.client import COARNotifyClient
from coarnotify.models.announce_endorsement import AnnounceEndorsement


class TestClient(TestCase):
    def test_01(self):
        client = COARNotifyClient()
        # inbox_url = client.discover("https://example.org")
        inbox_url = "http://localhost:5005/inbox"
        ae = AnnounceEndorsement()
        resp = client.send(inbox_url, ae)
        assert resp.action in [resp.CREATED, resp.ACCEPTED]
