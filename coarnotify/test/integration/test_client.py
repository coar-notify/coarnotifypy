from unittest import TestCase

from coarnotify.client import COARNotifyClient
from coarnotify.models.accept import Accept
from coarnotify.test.fixtures.accept import AcceptFixtureFactory
from coarnotify.models.announce_endorsement import AnnounceEndorsement

INBOX = "http://localhost:5005/inbox"


class TestClient(TestCase):
    def test_01_accept(self):
        client = COARNotifyClient(INBOX)
        source = AcceptFixtureFactory.source()
        acc = Accept(source)
        resp = client.send(acc)
        assert resp.action == resp.CREATED
        assert resp.location is not None
        print(resp.location)
