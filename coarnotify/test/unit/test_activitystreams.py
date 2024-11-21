from unittest import TestCase
from copy import deepcopy

from coarnotify.core.activitystreams2 import ActivityStream, Properties
from coarnotify.test.fixtures.announce_endorsement import AnnounceEndorsementFixtureFactory


class TestActivitystreams(TestCase):
    def test_01_construction(self):
        as2 = ActivityStream()
        assert as2.doc == {}
        assert as2.context == []

        source = AnnounceEndorsementFixtureFactory.source()
        s2 = deepcopy(source)
        s2context = s2.pop("@context")

        as2 = ActivityStream(source)

        assert as2.doc == s2
        assert as2.context == s2context

    def test_02_set_properties(self):
        as2 = ActivityStream()

        # properties that are just basic json
        as2.set_property("random", "value")
        assert as2.doc["random"] == "value"
        assert as2.context == []

        # properties that are in the ASProperties
        as2.set_property(Properties.ID, "value")
        assert as2.doc["id"] == "value"
        assert as2.context == [Properties.ID[1]]

        as2.set_property(Properties.TYPE, "another")
        assert as2.doc["type"] == "another"
        assert as2.context == [Properties.ID[1]]

        # other variations on property namespaces
        as2.set_property(("object", "http://example.com"), "object value")
        as2.set_property(("subject", "http://example.com"), "subject value")
        assert as2.doc["object"] == "object value"
        assert as2.doc["subject"] == "subject value"
        assert as2.context == [Properties.ID[1], "http://example.com"]

        as2.set_property(("foaf:name", ("foaf", "http://xmlns.com/foaf/0.1")), "name value")
        as2.set_property(("foaf:email", ("foaf", "http://xmlns.com/foaf/0.1")), "email value")
        assert as2.doc["foaf:name"] == "name value"
        assert as2.doc["foaf:email"] == "email value"
        assert as2.context == [Properties.ID[1], "http://example.com", {"foaf": "http://xmlns.com/foaf/0.1"}]

    def test_03_get_properties(self):
        as2 = ActivityStream()
        as2.set_property("random", "value")
        as2.set_property(Properties.ID, "id")
        as2.set_property(("object", "http://example.com"), "object value")
        as2.set_property(("foaf:name", ("foaf", "http://xmlns.com/foaf/0.1")), "name value")

        assert as2.get_property("random") == "value"
        assert as2.get_property(Properties.ID) == "id"
        assert as2.get_property(("object", "http://example.com")) == "object value"
        assert as2.get_property("object") == "object value"
        assert as2.get_property(("foaf:name", ("foaf", "http://xmlns.com/foaf/0.1"))) == "name value"
        assert as2.get_property("foaf:name") == "name value"

    def test_04_to_jsonld(self):
        # check we can round trip a document
        source = AnnounceEndorsementFixtureFactory.source()
        s2 = deepcopy(source)
        as2 = ActivityStream(source)
        assert as2.to_jsonld() == s2

        # check we can build a document from scratch and get an expected result
        as2 = ActivityStream()
        as2.set_property("random", "value")
        as2.set_property(Properties.ID, "id")
        as2.set_property(("object", "http://example.com"), "object value")
        as2.set_property(("foaf:name", ("foaf", "http://xmlns.com/foaf/0.1")), "name value")

        expected = {
            "@context": [Properties.ID[1], "http://example.com", {"foaf": "http://xmlns.com/foaf/0.1"}],
            "random": "value",
            "id": "id",
            "object": "object value",
            "foaf:name": "name value"
        }

        assert as2.to_jsonld() == expected
