from unittest import TestCase

from coarnotify.models import NotifyDocument, NotifyService, NotifyObject, NotifyActor, NotifyItem
from coarnotify.models import Accept, AnnounceEndorsement, AnnounceIngest, AnnounceRelationship
from coarnotify.test.fixtures.notify import NotifyFixtureFactory
from coarnotify.test.fixtures.accept import AcceptFixtureFactory
from coarnotify.test.fixtures.announce_endorsement import AnnounceEndorsementFixtureFactory
from coarnotify.test.fixtures.announce_ingest import AnnounceIngestFixtureFactory
from coarnotify.test.fixtures.announce_relationship import AnnounceRelationshipFixtureFactory


class TestModels(TestCase):
    def test_01_notify_manual_construct(self):
        n = NotifyDocument()

        # check the default properties
        assert n.id is not None
        assert n.id.startswith("urn:uuid:")
        assert n.type == NotifyDocument.TYPE
        assert n.origin is None
        assert n.target is None
        assert n.object is None
        assert n.actor is None
        assert n.in_reply_to is None
        assert n.context is None

        # now check the setters
        n.id = "whatever"
        n.type = "Other"

        origin = NotifyService()
        assert origin.id is not None
        assert origin.type == origin.DEFAULT_TYPE
        origin.inbox = "http://origin.com/inbox"
        n.origin = origin

        target = NotifyService()
        target.inbox = "http://target.com/inbox"
        n.target = target

        obj = NotifyObject()
        assert obj.id is not None
        assert obj.type is None
        n.object = obj

        actor = NotifyActor()
        assert actor.id is not None
        assert actor.type == actor.DEFAULT_TYPE
        n.actor = actor

        n.in_reply_to = "irt"

        context = NotifyObject()
        assert context.id is not None
        assert context.type is None
        n.context = context

        assert n.id == "whatever"
        assert n.type == "Other"
        assert n.origin.id == origin.id
        assert n.origin.type == origin.DEFAULT_TYPE
        assert n.origin.inbox == "http://origin.com/inbox"
        assert n.target.id == target.id
        assert n.target.type == target.DEFAULT_TYPE
        assert n.target.inbox == "http://target.com/inbox"
        assert n.object.id == obj.id
        assert n.object.type is None
        assert n.actor.id == actor.id
        assert n.actor.type == actor.DEFAULT_TYPE
        assert n.in_reply_to == "irt"
        assert n.context.id == context.id
        assert n.context.type is None

    def test_02_notify_from_fixture(self):
        source = NotifyFixtureFactory.source()
        n = NotifyDocument(source)

        # now check we've got all the source properties
        assert n.id == source["id"]
        assert n.type == source["type"]
        assert isinstance(n.origin, NotifyService)
        assert n.origin.id == source["origin"]["id"]
        assert isinstance(n.object, NotifyObject)
        assert n.object.id == source["object"]["id"]
        assert isinstance(n.target, NotifyService)
        assert n.target.id == source["target"]["id"]
        assert isinstance(n.actor, NotifyActor)
        assert n.actor.id == source["actor"]["id"]
        assert n.in_reply_to == source["inReplyTo"]
        assert isinstance(n.context, NotifyObject)
        assert n.context.id == source["context"]["id"]
        assert isinstance(n.context.item, NotifyItem)
        assert n.context.item.id == source["context"]["ietf:item"]["id"]

        # now check we can rewrite some properties
        n.id = "whatever"
        n.type = "Other"
        assert n.id == "whatever"
        assert n.type == "Other"

    def test_03_notify_operations(self):
        n = NotifyDocument()
        assert n.validate() is False
        assert n.to_dict() is not None

        source = NotifyFixtureFactory.source()
        n = NotifyDocument(source)
        assert n.validate() is True
        assert n.to_dict() == source

    def test_04_accept(self):
        a = Accept()
        source = AcceptFixtureFactory.source()
        a = Accept(source)
        assert a.validate() is True
        assert a.to_dict() == source

    def test_05_announce_endorsement(self):
        ae = AnnounceEndorsement()
        source = AnnounceEndorsementFixtureFactory.source()
        ae = AnnounceEndorsement(source)
        assert ae.validate() is True
        assert ae.to_dict() == source

    def test_06_announce_ingest(self):
        ai = AnnounceIngest()
        source = AnnounceIngestFixtureFactory.source()
        ai = AnnounceIngest(source)
        assert ai.validate() is True
        assert ai.to_dict() == source

    def test_07_announce_relationship(self):
        ae = AnnounceRelationship()

        source = AnnounceRelationshipFixtureFactory.source()
        ae = AnnounceRelationship(source)
        assert ae.validate() is True
        assert ae.to_dict() == source

        # now test we are properly reading the fixture
        assert ae.actor.id == "https://research-organisation.org"
        assert ae.actor.name == "Research Organisation"
        assert ae.actor.type == "Organization"

        assert ae.context.id == "https://another-research-organisation.org/repository/datasets/item/201203421/"
        assert ae.context.cite_as == "https://doi.org/10.5555/999555666"
        item = ae.context.item
        assert item.id == "https://another-research-organisation.org/repository/datasets/item/201203421/data_archive.zip"
        assert item.media_type == "application/zip"
        assert item.type == ["Article", "sorg:Dataset"]

        assert ae.id == "urn:uuid:94ecae35-dcfd-4182-8550-22c7164fe23f"
        assert ae.type == ["Announce", "coar-notify:RelationshipAction"]

        assert ae.object.id == "urn:uuid:74FFB356-0632-44D9-B176-888DA85758DC"
        assert ae.object.type == "Relationship"
        triple = ae.object.triple
        assert triple[0] == "https://another-research-organisation.org/repository/datasets/item/201203421/"
        assert triple[1] == "http://purl.org/vocab/frbr/core#supplement"
        assert triple[2] == "https://research-organisation.org/repository/item/201203/421/"

        assert ae.origin.id == "https://research-organisation.org/repository"
        assert ae.origin.inbox == "https://research-organisation.org/inbox/"
        assert ae.origin.type == "Service"

        assert ae.target.id == "https://another-research-organisation.org/repository"
        assert ae.target.inbox == "https://another-research-organisation.org/inbox/"
        assert ae.target.type == "Service"

