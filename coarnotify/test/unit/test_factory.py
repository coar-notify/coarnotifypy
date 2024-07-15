from unittest import TestCase

from coarnotify.models import Accept, AnnounceEndorsement, AnnounceIngest, AnnounceRelationship
from coarnotify.common import COARNotifyFactory

from coarnotify.test.fixtures import AcceptFixtureFactory, AnnounceEndorsementFixtureFactory, AnnounceIngestFixtureFactory, AnnounceRelationshipFixtureFactory


class TestFactory(TestCase):
    def test_01_accept(self):
        acc = COARNotifyFactory.get_by_types(Accept.TYPE)
        assert acc == Accept

        source = AcceptFixtureFactory.source()
        acc = COARNotifyFactory.get_by_object(source)
        assert isinstance(acc, Accept)

        assert acc.id == source["id"]

    def test_02_announce_endorsement(self):
        ae = COARNotifyFactory.get_by_types(AnnounceEndorsement.TYPE)
        assert ae == AnnounceEndorsement

        source = AnnounceEndorsementFixtureFactory.source()
        ae = COARNotifyFactory.get_by_object(source)
        assert isinstance(ae, AnnounceEndorsement)

        assert ae.id == source["id"]

    def test_03_announce_ingest(self):
        ai = COARNotifyFactory.get_by_types(AnnounceIngest.TYPE)
        assert ai == AnnounceIngest

        source = AnnounceIngestFixtureFactory.source()
        ai = COARNotifyFactory.get_by_object(source)
        assert isinstance(ai, AnnounceIngest)

        assert ai.id == source["id"]

    def test_04_announce_relationship(self):
        ar = COARNotifyFactory.get_by_types(AnnounceRelationship.TYPE)
        assert ar == AnnounceRelationship

        source = AnnounceRelationshipFixtureFactory.source()
        ar = COARNotifyFactory.get_by_object(source)
        assert isinstance(ar, AnnounceRelationship)

        assert ar.id == source["id"]
