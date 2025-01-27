from unittest import TestCase

from coarnotify.core.notify import NotifyPattern, NotifyService, NotifyObject
from coarnotify.patterns import (
    Accept,
    AnnounceEndorsement,
    AnnounceRelationship,
    AnnounceReview,
    AnnounceServiceResult,
    RequestEndorsement,
    RequestReview,
    TentativelyAccept,
    TentativelyReject,
    UnprocessableNotification,
    UndoOffer,
    Reject
)
from coarnotify.test.fixtures.notify import NotifyFixtureFactory
from coarnotify.test.fixtures import (
    AcceptFixtureFactory,
    AnnounceEndorsementFixtureFactory,
    AnnounceRelationshipFixtureFactory,
    AnnounceReviewFixtureFactory,
    AnnounceServiceResultFixtureFactory,
    RequestReviewFixtureFactory,
    RequestEndorsementFixtureFactory,
    URIFixtureFactory,
    TentativelyAcceptFixtureFactory,
    TentativelyRejectFixtureFactory,
    UnprocessableNotificationFixtureFactory,
    UndoOfferFixtureFactory,
    RejectFixtureFactory
)

from coarnotify.exceptions import ValidationError
from coarnotify.core.activitystreams2 import Properties
from coarnotify.core.notify import NotifyProperties
from coarnotify import validate
from coarnotify.validate import Validator


class TestValidate(TestCase):
    def test_01_structural_empty(self):
        n = NotifyPattern()
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
        n = NotifyPattern()
        with self.assertRaises(ValidationError) as ve:
            n.validate()

        errors = ve.exception.errors
        assert Properties.ID not in errors
        assert Properties.TYPE not in errors
        assert Properties.OBJECT in errors
        assert Properties.TARGET in errors
        assert Properties.ORIGIN in errors

    def test_03_structural_valid_document(self):
        n = NotifyPattern()
        n.target = NotifyFixtureFactory.target()
        n.origin = NotifyFixtureFactory.origin()
        n.object = NotifyFixtureFactory.object()

        assert n.validate() is True

    def test_04_structural_invalid_nested(self):
        n = NotifyPattern()
        n.target = NotifyService({"whatever": "value"}, validate_stream_on_construct=False)
        n.origin = NotifyService({"another": "junk"}, validate_stream_on_construct=False)
        n.object = NotifyObject({"yet": "more"}, validate_stream_on_construct=False)

        with self.assertRaises(ValidationError) as ve:
            n.validate()

        errors = ve.exception.errors
        assert Properties.ID not in errors
        assert Properties.TYPE not in errors
        assert Properties.OBJECT not in errors  # the object is present, and will acquire an id, so will not be in the errors
        assert Properties.TARGET in errors
        assert Properties.ORIGIN in errors

        # These are no longer causing validation errors, as the index field is not being checked

        # target = errors[Properties.TARGET]
        # assert len(target.get("errors")) == 0
        # assert target.get("nested") is not None
        # assert NotifyProperties.INBOX in target.get("nested")

        # origin = errors[Properties.ORIGIN]
        # assert len(origin.get("errors")) == 0
        # assert origin.get("nested") is not None
        # assert NotifyProperties.INBOX in origin.get("nested")

    def test_05_validation_modes(self):
        valid = NotifyFixtureFactory.source()
        n = NotifyPattern(stream=valid, validate_stream_on_construct=True)

        invalid = NotifyFixtureFactory.source()
        invalid["id"] = "http://example.com/^path"
        with self.assertRaises(ValidationError) as ve:
            n = NotifyPattern(stream=invalid, validate_stream_on_construct=True)
        assert ve.exception.errors.get(Properties.ID) is not None

        valid = NotifyFixtureFactory.source()
        n = NotifyPattern(stream=valid, validate_stream_on_construct=False)

        invalid = NotifyFixtureFactory.source()
        invalid["id"] = "http://example.com/^path"
        n = NotifyPattern(stream=invalid, validate_stream_on_construct=False)

        n = NotifyPattern(validate_properties=False)
        n.id = "urn:uuid:4fb3af44-d4f8-4226-9475-2d09c2d8d9e0"  # valid
        n.id = "http://example.com/^path"   # invalid

        with self.assertRaises(ValidationError) as ve:
            n.validate()
        assert ve.exception.errors.get(Properties.ID) is not None

    def test_06_validate_id_property(self):
        n = NotifyPattern()
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

    def test_07_validate_url(self):
        urls = URIFixtureFactory.generate(schemes=["http", "https"])
        # print(urls)

        for url in urls:
            # print(url)
            assert validate.url(None, url) is True

        with self.assertRaises(ValueError):
            validate.url(None, "ftp://example.com")
        with self.assertRaises(ValueError):
            validate.url(None, "http:/example.com")
        with self.assertRaises(ValueError):
            validate.url(None, "http://domain/path")
        with self.assertRaises(ValueError):
            validate.url(None, "http://example.com/path^wrong")

    def test_08_one_of(self):
        values = ["a", "b", "c"]
        validator = validate.one_of(values)
        assert validator(None, "a") is True
        assert validator(None, "b") is True
        assert validator(None, "c") is True

        with self.assertRaises(ValueError):
            validator(None, "d")

        with self.assertRaises(ValueError):
            # one_of expects a singular value, it does not do lists
            validator(None, ["a", "b"])

    def test_09_contains(self):
        validator = validate.contains("a")
        assert validator(None, ["a", "b", "c"]) is True

        with self.assertRaises(ValueError):
            validator(None, ["b", "c", "d"])

    def test_10_at_least_one_of(self):
        values = ["a", "b", "c"]
        validator = validate.at_least_one_of(values)
        assert validator(None, "a") is True
        assert validator(None, "b") is True
        assert validator(None, "c") is True

        with self.assertRaises(ValueError):
            validator(None, "d")

        # at_least_one_of can take a list and validate each one against the global criteria
        assert validator(None, ["a", "d"]) is True

    ########################################
    ## validation methods for specific patterns

    def _base_validate(self, a):
        # now try to apply invalid values to it
        with self.assertRaises(ValueError):
            a.id = "not a uri"

        with self.assertRaises(ValueError):
            a.in_reply_to = "not a uri"

        with self.assertRaises(ValueError):
            # not an HTTP URI
            a.origin.id = "urn:uuid:4fb3af44-d4f8-4226-9475-2d09c2d8d9e0"

        with self.assertRaises(ValueError):
            a.origin.inbox = "not a uri"

        with self.assertRaises(ValueError):
            # not an HTTP URI
            a.target.id = "urn:uuid:4fb3af44-d4f8-4226-9475-2d09c2d8d9e0"

        with self.assertRaises(ValueError):
            a.target.inbox = "not a uri"

        with self.assertRaises(ValueError):
            a.type = "NotAValidType"

    def _actor_validate(self, a):
        with self.assertRaises(ValueError):
            a.actor.id = "not a uri"

        with self.assertRaises(ValueError):
            a.actor.type = "NotAValidType"

    def _object_validate(self, a):
        with self.assertRaises(ValueError):
            a.object.id = "not a uri"

        with self.assertRaises(ValueError):
            a.object.cite_as = "urn:uuid:4fb3af44-d4f8-4226-9475-2d09c2d8d9e0"

    def _context_validate(self, a):
        with self.assertRaises(ValueError):
            a.context.id = "not a uri"

        with self.assertRaises(ValueError):
            a.context.type = "NotAValidType"

        with self.assertRaises(ValueError):
            a.context.cite_as = "urn:uuid:4fb3af44-d4f8-4226-9475-2d09c2d8d9e0"

    def test_11_accept_validate(self):
        # make a valid one
        source = AcceptFixtureFactory.source()
        a = Accept(source)

        self._base_validate(a)

        # now make one with fully invalid data
        isource = AcceptFixtureFactory.invalid()
        with self.assertRaises(ValidationError) as ve:
            a = Accept(isource)

    def test_12_announce_endorsement_validate(self):
        # make a valid one
        source = AnnounceEndorsementFixtureFactory.source()
        a = AnnounceEndorsement(source)

        self._base_validate(a)

        with self.assertRaises(ValueError):
            # one of the required types, but not both of them
            a.type = "Announce"

        self._actor_validate(a)
        self._object_validate(a)
        self._context_validate(a)

        # now make one with fully invalid data
        isource = AnnounceEndorsementFixtureFactory.invalid()
        with self.assertRaises(ValidationError) as ve:
            a = AnnounceEndorsement(isource)

    def test_13_tentative_accept_validate(self):
        # make a valid one
        source = TentativelyAcceptFixtureFactory.source()
        a = TentativelyAccept(source)

        self._base_validate(a)
        self._actor_validate(a)
        # omit object validation, as the nested object here is a full notification in its own right
        # self._object_validate(a)

        # now make one with fully invalid data
        isource = TentativelyAcceptFixtureFactory.invalid()
        with self.assertRaises(ValidationError) as ve:
            a = TentativelyAccept(isource)

    def test_14_tentative_reject_validate(self):
        # make a valid one
        source = TentativelyRejectFixtureFactory.source()
        a = TentativelyReject(source)

        self._base_validate(a)
        self._actor_validate(a)
        # omit object validation, as the nested object here is a full notification in its own right
        # self._object_validate(a)

        # now make one with fully invalid data
        isource = TentativelyRejectFixtureFactory.invalid()
        with self.assertRaises(ValidationError) as ve:
            a = TentativelyReject(isource)

    def test_15_unprocessable_notification_validate(self):
        # make a valid one
        source = UnprocessableNotificationFixtureFactory.source()
        a = UnprocessableNotification(source)

        self._base_validate(a)
        self._actor_validate(a)
        # self._object_validate(a)

        # now make one with fully invalid data
        isource = UnprocessableNotificationFixtureFactory.invalid()
        with self.assertRaises(ValidationError) as ve:
            a = UnprocessableNotification(isource)

    def test_16_undo_offer_validate(self):
        # make a valid one
        source = UndoOfferFixtureFactory.source()
        a = UndoOffer(source)

        self._base_validate(a)
        self._actor_validate(a)
        # self._object_validate(a)

        # now make one with fully invalid data
        isource = UndoOfferFixtureFactory.invalid()
        with self.assertRaises(ValidationError) as ve:
            a = UnprocessableNotification(isource)


    def test_17_announce_review_validate(self):
        # make a valid one
        source = AnnounceReviewFixtureFactory.source()
        a = AnnounceReview(source)

        self._base_validate(a)

        with self.assertRaises(ValueError):
            # one of the required types, but not both of them
            a.type = "Offer"

        self._actor_validate(a)
        self._object_validate(a)

        # now make one with fully invalid data
        isource = AnnounceReviewFixtureFactory.invalid()
        with self.assertRaises(ValidationError) as ve:
            a = AnnounceReview(isource)

    def test_18_request_endorsement_validate(self):
        # make a valid one
        source = RequestEndorsementFixtureFactory.source()
        a = RequestEndorsement(source)

        self._base_validate(a)
        self._actor_validate(a)
        self._object_validate(a)

        with self.assertRaises(ValueError):
            # one of the required types, but not both of them
            a.type = "Offer"

        # now make one with fully invalid data
        isource = RequestEndorsementFixtureFactory.invalid()
        with self.assertRaises(ValidationError) as ve:
            a = RequestEndorsement(isource)

    def test_19_request_review_validate(self):
        # make a valid one
        source = RequestReviewFixtureFactory.source()
        a = RequestReview(source)

        self._base_validate(a)
        self._actor_validate(a)
        self._object_validate(a)

        with self.assertRaises(ValueError):
            # one of the required types, but not both of them
            a.type = "Offer"

        # now make one with fully invalid data
        isource = RequestReviewFixtureFactory.invalid()
        with self.assertRaises(ValidationError) as ve:
            a = RequestReview(isource)

    def test_20_reject_validate(self):
        # make a valid one
        source = RejectFixtureFactory.source()
        a = Reject(source)

        self._base_validate(a)
        self._actor_validate(a)
        # self._object_validate(a)

        # now make one with fully invalid data
        isource = RejectFixtureFactory.invalid()
        with self.assertRaises(ValidationError) as ve:
            a = Reject(isource)

    def test_21_announce_relationship_validate(self):
        # make a valid one
        source = AnnounceRelationshipFixtureFactory.source()
        a = AnnounceRelationship(source)

        self._base_validate(a)
        self._actor_validate(a)
        self._object_validate(a)
        self._context_validate(a)

        with self.assertRaises(ValueError):
            # one of the required types, but not both of them
            a.type = "Announce"

        # now make one with fully invalid data
        isource = AnnounceRelationshipFixtureFactory.invalid()
        with self.assertRaises(ValidationError) as ve:
            a = AnnounceRelationship(isource)

    def test_21_announce_service_result_validate(self):
        # make a valid one
        source = AnnounceServiceResultFixtureFactory.source()
        a = AnnounceServiceResult(source)

        self._base_validate(a)
        self._actor_validate(a)
        self._object_validate(a)
        self._context_validate(a)

        # now make one with fully invalid data
        isource = AnnounceServiceResultFixtureFactory.invalid()
        with self.assertRaises(ValidationError) as ve:
            a = AnnounceServiceResult(isource)

    def test_22_add_rules(self):
        rules = {
            Properties.ID: {
                "default": validate.absolute_uri,
                "context": {
                    Properties.CONTEXT: {
                        "default": validate.url
                    },
                    Properties.ORIGIN: {
                        "default": validate.url
                    },
                    Properties.TARGET: {
                        "default": validate.url
                    },
                    NotifyProperties.ITEM: {
                        "default": validate.url
                    }
                }
            },
            Properties.TYPE: {
                "default": validate.type_checker,
            }
        }

        v = Validator(rules)

        update = {
            Properties.ID: {
                "default": validate.url
            },
            Properties.TYPE: {
                "context": {
                    Properties.CONTEXT: {
                        "default": validate.url
                    }
                }
            },
            Properties.ACTOR : {
                "default": validate.url
            }
        }

        v.add_rules(update)

        rules = v.rules()
        assert rules[Properties.ID]["default"] == validate.url
        assert rules[Properties.ID]["context"][Properties.CONTEXT]["default"] == validate.url
        assert rules[Properties.TYPE]["default"] == validate.type_checker
        assert rules[Properties.TYPE]["context"][Properties.CONTEXT]["default"] == validate.url
        assert rules[Properties.ACTOR]["default"] == validate.url
