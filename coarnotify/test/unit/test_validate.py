from unittest import TestCase
from copy import deepcopy

from coarnotify.models import NotifyDocument, NotifyService, NotifyObject, NotifyActor, NotifyItem
from coarnotify.models import (
    Accept,
    AnnounceEndorsement,
    AnnounceIngest,
    AnnounceRelationship,
    AnnounceReview,
    AnnounceServiceResult
)
from coarnotify.test.fixtures.notify import NotifyFixtureFactory
from coarnotify.test.fixtures import (
    AcceptFixtureFactory,
    AnnounceEndorsementFixtureFactory,
    AnnounceIngestFixtureFactory,
    AnnounceRelationshipFixtureFactory,
    AnnounceReviewFixtureFactory,
    AnnounceServiceResultFixtureFactory
)

from coarnotify.exceptions import ValidationError
from coarnotify.activitystreams2.activitystreams2 import Properties
from coarnotify.models.notify import NotifyProperties


class TestValidate(TestCase):
    def test_01_structural_empty(self):
        n = NotifyDocument()
        n.id = None     # these are automatically set, so remove them to trigger validation
        n.type = None
        with self.assertRaises(ValidationError) as ve:
            n.validate()

        errors = ve.exception.errors
        assert Properties.ID in errors
        assert Properties.TYPE in errors
        assert Properties.OBJECT in errors
        assert Properties.TARGET in errors
        assert Properties.ORIGIN in errors

    def test_02_structural_basic(self):
        n = NotifyDocument()
        with self.assertRaises(ValidationError) as ve:
            n.validate()

        errors = ve.exception.errors
        assert Properties.ID not in errors
        assert Properties.TYPE not in errors
        assert Properties.OBJECT in errors
        assert Properties.TARGET in errors
        assert Properties.ORIGIN in errors

    def test_03_structural_valid_document(self):
        n = NotifyDocument()
        n.target = NotifyFixtureFactory.target()
        n.origin = NotifyFixtureFactory.origin()
        n.object = NotifyFixtureFactory.object()

        assert n.validate() is True

    def test_04_structural_invalid_nested(self):
        n = NotifyDocument()
        n.target = NotifyService({"whatever": "value"}, validate_stream_on_construct=False)
        n.origin = NotifyService({"another": "junk"}, validate_stream_on_construct=False)
        n.object = NotifyObject({"yet": "more"}, validate_stream_on_construct=False)

        with self.assertRaises(ValidationError) as ve:
            n.validate()

        errors = ve.exception.errors
        assert Properties.ID not in errors
        assert Properties.TYPE not in errors
        assert Properties.OBJECT in errors
        assert Properties.TARGET in errors
        assert Properties.ORIGIN in errors

        target = errors[Properties.TARGET]
        assert len(target.get("errors")) == 0
        assert target.get("nested") is not None
        assert NotifyProperties.INBOX in target.get("nested")

        origin = errors[Properties.ORIGIN]
        assert len(origin.get("errors")) == 0
        assert origin.get("nested") is not None
        assert NotifyProperties.INBOX in origin.get("nested")

        object = errors[Properties.OBJECT]
        assert len(object.get("errors")) == 0
        assert object.get("nested") is not None
        assert Properties.TYPE in object.get("nested")

    def test_05_validation_modes(self):
        valid = NotifyFixtureFactory.source()
        n = NotifyDocument(stream=valid, validate_stream_on_construct=True)

        invalid = NotifyFixtureFactory.source()
        invalid["id"] = "http://example.com/^path"
        with self.assertRaises(ValidationError) as ve:
            n = NotifyDocument(stream=invalid, validate_stream_on_construct=True)
        assert ve.exception.errors.get(Properties.ID) is not None

        valid = NotifyFixtureFactory.source()
        n = NotifyDocument(stream=valid, validate_stream_on_construct=False)

        invalid = NotifyFixtureFactory.source()
        invalid["id"] = "http://example.com/^path"
        n = NotifyDocument(stream=invalid, validate_stream_on_construct=False)

        n = NotifyDocument(validate_properties=False)
        n.id = "urn:uuid:4fb3af44-d4f8-4226-9475-2d09c2d8d9e0"  # valid
        n.id = "http://example.com/^path"   # invalid

        with self.assertRaises(ValidationError) as ve:
            n.validate()
        assert ve.exception.errors.get(Properties.ID) is not None

    def test_06_validate_id_property(self):
        n = NotifyDocument()
        # test the various ways it can fail:
        with self.assertRaises(ValueError) as ve:
            n.id = "9whatever:none"
        assert ve.exception.args[0] == "Invalid URI scheme `9whatever`"

        with self.assertRaises(ValueError) as ve:
            n.id = "http://wibble/stuff"
        assert ve.exception.args[0] == "Invalid URI authority `wibble`"

        with self.assertRaises(ValueError) as ve:
            n.id = "http://example.com/^path"
        assert ve.exception.args[0] == "Invalid URI path `/^path`"

        with self.assertRaises(ValueError) as ve:
            n.id = "http://example.com/path/here/?^=what"
        assert ve.exception.args[0] == "Invalid URI query `^=what`"

        with self.assertRaises(ValueError) as ve:
            n.id = "http://example.com/path/here/?you=what#^frag"
        assert ve.exception.args[0] == "Invalid URI fragment `^frag`"

        # test a bunch of successful ones

        # These ones taken from wikipedia
        n.id = "https://john.doe@www.example.com:1234/forum/questions/?tag=networking&order=newest#top"
        n.id = "https://john.doe@www.example.com:1234/forum/questions/?tag=networking&order=newest#:~:text=whatever"
        n.id = "ldap://[2001:db8::7]/c=GB?objectClass?one"
        n.id = "mailto:John.Doe@example.com"
        n.id = "news:comp.infosystems.www.servers.unix"
        n.id = "tel:+1-816-555-1212"
        n.id = "telnet://192.0.2.16:80/"
        n.id = "urn:oasis:names:specification:docbook:dtd:xml:4.1.2"

        # these ones taken from the spec
        n.id = "urn:uuid:4fb3af44-d4f8-4226-9475-2d09c2d8d9e0"
        n.id = "https://generic-service.com/system"
        n.id = "https://generic-service.com/system/inbox/"

