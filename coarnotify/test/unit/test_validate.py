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
        n.target = NotifyService({"whatever": "value"})
        n.origin = NotifyService({"another": "junk"})
        n.object = NotifyObject({"yet": "more"})

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

