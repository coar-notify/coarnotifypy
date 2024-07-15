from unittest import TestCase

from coarnotify.client import COARNotifyClient
from coarnotify.models.announce_endorsement import AnnounceEndorsement
from coarnotify.test.mocks.http import MockHttpResponse, MockHttpLayer


class TestClient(TestCase):
    def test_01_construction(self):
        client = COARNotifyClient()
        assert client.inbox_url is None

        client = COARNotifyClient("http://example.com/inbox")
        assert client.inbox_url == "http://example.com/inbox"

        client = COARNotifyClient(http_layer=MockHttpLayer())
        client = COARNotifyClient("http://example.com/inbox", MockHttpLayer())

    def test_02_created_response(self):
        client = COARNotifyClient("http://example.com/inbox", MockHttpLayer(
            status_code=201,
            location="http://example.com/location"
        ))
        ae = AnnounceEndorsement()
        resp = client.send(ae)
        assert resp.action == resp.CREATED
        assert resp.location == "http://example.com/location"

        # inbox_url = client.discover("https://example.org")
        # inbox_url = "http://localhost:5005/inbox"
        # ae = AnnounceEndorsement()
        # resp = client.send(inbox_url, ae)
        # assert resp.action in [resp.CREATED, resp.ACCEPTED]

    def test_03_accepted_response(self):
        client = COARNotifyClient("http://example.com/inbox", MockHttpLayer(
            status_code=202
        ))
        ae = AnnounceEndorsement()
        resp = client.send(ae)
        assert resp.action == resp.ACCEPTED
        assert resp.location is None
