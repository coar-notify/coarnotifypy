from unittest import TestCase

from coarnotify.models.notify import Notify, NotifyService, NotifyObject, NotifyActor, NotifyContext
from coarnotify.models.accept import Accept
from coarnotify.models.announce_endorsement import AnnounceEndorsement
from coarnotify.test.fixtures.notify import NotifyFixtureFactory
from coarnotify.test.fixtures.accept import AcceptFixtureFactory
from coarnotify.test.fixtures.announce_endorsement import AnnounceEndorsementFixtureFactory


class TestNotify(TestCase):
    def test_01_notify_manual_construct(self):
        n = Notify()

        # check the default properties
        assert n.id is not None
        assert n.id.startswith("urn:uuid:")
        assert n.type == Notify.DEFAULT_TYPE
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
        assert obj.type != obj.DEFAULT_TYPE
        n.object = obj

        actor = NotifyActor()
        assert actor.id is not None
        assert actor.type != actor.DEFAULT_TYPE
        n.actor = actor

        n.in_reply_to = "irt"

        context = NotifyContext()
        assert context.id is not None
        assert context.type != context.DEFAULT_TYPE
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
        assert n.object.type != obj.DEFAULT_TYPE
        assert n.actor.id == actor.id
        assert n.actor.type != actor.DEFAULT_TYPE
        assert n.in_reply_to == "irt"
        assert n.context.id == context.id
        assert n.context.type != context.DEFAULT_TYPE

    def test_02_notify_from_fixture(self):
        source = NotifyFixtureFactory.source()
        n = Notify(source)

        # now check we've got all the source properties
        assert n.id == source["id"]
        assert n.type == source["type"]
        assert n.origin.id == source["origin"]["id"]
        assert n.object.id == source["object"]["id"]
        assert n.target.id == source["target"]["id"]
        assert n.actor.id == source["actor"]["id"]
        assert n.in_reply_to == source["inReplyTo"]
        assert n.context.id == source["context"]["id"]

        # now check we can rewrite some properties
        n.id = "whatever"
        n.type = "Other"
        assert n.id == "whatever"
        assert n.type == "Other"

    def test_03_notify_operations(self):
        n = Notify()
        assert n.validate() is False
        assert n.to_dict() is not None

        source = NotifyFixtureFactory.source()
        n = Notify(source)
        assert n.validate() is True
        assert n.to_dict() == source

    def test_04_accept(self):
        a = Accept()
        # Accept is the same as the base Notify class, so don't need to test it beyond
        # construction

        source = AcceptFixtureFactory.source()
        a = Accept(source)
        assert a.validate() is True
        assert a.to_dict() == source

    def test_05_announce_endorsement(self):
        ae = AnnounceEndorsement()
        # Accept is the same as the base Notify class, so don't need to test it beyond
        # construction

        source = AnnounceEndorsementFixtureFactory.source()
        ae = AnnounceEndorsement(source)
        assert ae.validate() is True
        assert ae.to_dict() == source