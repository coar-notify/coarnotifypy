"""Test cases for the COARNotifyClient class."""

from unittest import TestCase

from coarnotify.client import COARNotifyClient
from coarnotify.patterns import AnnounceEndorsement
from coarnotify.test.fixtures import AnnounceEndorsementFixtureFactory
from coarnotify.test.mocks.http import MockHttpLayer


class TestClient(TestCase):
    """Test the COARNotifyClient class."""

    def test_01_construction(self):
        """Test the construction of a COARNotifyClient object."""
        client = COARNotifyClient()
        assert client.inbox_url is None

        client = COARNotifyClient("http://example.com/inbox")
        assert client.inbox_url == "http://example.com/inbox"

        client = COARNotifyClient(http_layer=MockHttpLayer())
        client = COARNotifyClient("http://example.com/inbox", MockHttpLayer())

    def test_02_created_response(self):
        """Test the response to a created resource."""
        client = COARNotifyClient(
            "http://example.com/inbox", MockHttpLayer(status_code=201, location="http://example.com/location")
        )
        source = AnnounceEndorsementFixtureFactory.source()
        ae = AnnounceEndorsement(source)
        resp = client.send(ae)
        assert resp.action == resp.CREATED
        assert resp.location == "http://example.com/location"

    def test_03_accepted_response(self):
        """Test the response to an accepted request."""
        client = COARNotifyClient("http://example.com/inbox", MockHttpLayer(status_code=202))
        source = AnnounceEndorsementFixtureFactory.source()
        ae = AnnounceEndorsement(source)
        resp = client.send(ae)
        assert resp.action == resp.ACCEPTED
        assert resp.location is None
