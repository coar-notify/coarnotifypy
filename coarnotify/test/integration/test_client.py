from unittest import TestCase

from coarnotify.client import COARNotifyClient
from coarnotify.models import Accept
from coarnotify.test.fixtures.accept import AcceptFixtureFactory

from coarnotify.models import AnnounceEndorsement
from coarnotify.test.fixtures.announce_endorsement import AnnounceEndorsementFixtureFactory

from coarnotify.models import AnnounceIngest
from coarnotify.test.fixtures.announce_ingest import AnnounceIngestFixtureFactory

from coarnotify.models import AnnounceRelationship
from coarnotify.test.fixtures.announce_relationship import AnnounceRelationshipFixtureFactory

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

    def test_02_announce_endorsement(self):
        client = COARNotifyClient(INBOX)
        source = AnnounceEndorsementFixtureFactory.source()
        ae = AnnounceEndorsement(source)
        resp = client.send(ae)
        assert resp.action == resp.CREATED
        assert resp.location is not None
        print(resp.location)

    def test_03_announce_ingest(self):
        client = COARNotifyClient(INBOX)
        source = AnnounceIngestFixtureFactory.source()
        ae = AnnounceIngest(source)
        resp = client.send(ae)
        assert resp.action == resp.CREATED
        assert resp.location is not None
        print(resp.location)

    def test_04_announce_relationship(self):
        client = COARNotifyClient(INBOX)
        source = AnnounceRelationshipFixtureFactory.source()
        ae = AnnounceRelationship(source)
        resp = client.send(ae)
        assert resp.action == resp.CREATED
        assert resp.location is not None
        print(resp.location)
