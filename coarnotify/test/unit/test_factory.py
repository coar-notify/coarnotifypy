"""Test cases for the factory module."""

from unittest import TestCase

from coarnotify.core.notify import NotifyPattern
from coarnotify.patterns import (
    Accept,
    AnnounceEndorsement,
    AnnounceRelationship,
    AnnounceReview,
    AnnounceServiceResult,
    Reject,
    RequestEndorsement,
    RequestReview,
    TentativelyAccept,
    TentativelyReject,
    UnprocessableNotification,
    UndoOffer,
)
from coarnotify.factory import COARNotifyFactory

from coarnotify.test.fixtures import (
    AcceptFixtureFactory,
    AnnounceEndorsementFixtureFactory,
    AnnounceRelationshipFixtureFactory,
    AnnounceReviewFixtureFactory,
    AnnounceServiceResultFixtureFactory,
    RejectFixtureFactory,
    RequestEndorsementFixtureFactory,
    RequestReviewFixtureFactory,
    TentativelyAcceptFixtureFactory,
    TentativelyRejectFixtureFactory,
    UnprocessableNotificationFixtureFactory,
    UndoOfferFixtureFactory,
)


class TestFactory(TestCase):
    """Test the COARNotifyFactory class."""

    def test_01_accept(self):
        """Accept a notification."""
        acc = COARNotifyFactory.get_by_types(Accept.TYPE)
        assert acc == Accept

        source = AcceptFixtureFactory.source()
        acc = COARNotifyFactory.get_by_object(source)
        assert isinstance(acc, Accept)

        assert acc.id == source["id"]

    def test_02_announce_endorsement(self):
        """Announce an endorsement."""
        ae = COARNotifyFactory.get_by_types(AnnounceEndorsement.TYPE)
        assert ae == AnnounceEndorsement

        source = AnnounceEndorsementFixtureFactory.source()
        ae = COARNotifyFactory.get_by_object(source)
        assert isinstance(ae, AnnounceEndorsement)

        assert ae.id == source["id"]

    def test_04_announce_relationship(self):
        """Announce a relationship."""
        ar = COARNotifyFactory.get_by_types(AnnounceRelationship.TYPE)
        assert ar == AnnounceRelationship

        source = AnnounceRelationshipFixtureFactory.source()
        ar = COARNotifyFactory.get_by_object(source)
        assert isinstance(ar, AnnounceRelationship)

        assert ar.id == source["id"]

    def test_05_announce_review(self):
        """Announce a review."""
        ar = COARNotifyFactory.get_by_types(AnnounceReview.TYPE)
        assert ar == AnnounceReview

        source = AnnounceReviewFixtureFactory.source()
        ar = COARNotifyFactory.get_by_object(source)
        assert isinstance(ar, AnnounceReview)

        assert ar.id == source["id"]

    def test_06_announce_service_result(self):
        """Announce a service result."""
        ar = COARNotifyFactory.get_by_types(AnnounceServiceResult.TYPE)
        assert ar == AnnounceServiceResult

        source = AnnounceServiceResultFixtureFactory.source()
        ar = COARNotifyFactory.get_by_object(source)
        assert isinstance(ar, AnnounceServiceResult)

        assert ar.id == source["id"]

    def test_07_reject(self):
        """Reject a notification."""
        ar = COARNotifyFactory.get_by_types(Reject.TYPE)
        assert ar == Reject

        source = RejectFixtureFactory.source()
        ar = COARNotifyFactory.get_by_object(source)
        assert isinstance(ar, Reject)

        assert ar.id == source["id"]

    def test_08_request_endorsement(self):
        """Request an endorsement."""
        ar = COARNotifyFactory.get_by_types(RequestEndorsement.TYPE)
        assert ar == RequestEndorsement

        source = RequestEndorsementFixtureFactory.source()
        ar = COARNotifyFactory.get_by_object(source)
        assert isinstance(ar, RequestEndorsement)

        assert ar.id == source["id"]

    def test_10_request_review(self):
        """Request a review."""
        ar = COARNotifyFactory.get_by_types(RequestReview.TYPE)
        assert ar == RequestReview

        source = RequestReviewFixtureFactory.source()
        ar = COARNotifyFactory.get_by_object(source)
        assert isinstance(ar, RequestReview)

        assert ar.id == source["id"]

    def test_11_tentatively_accept(self):
        """Tentatively accept a notification."""
        ar = COARNotifyFactory.get_by_types(TentativelyAccept.TYPE)
        assert ar == TentativelyAccept

        source = TentativelyAcceptFixtureFactory.source()
        ar = COARNotifyFactory.get_by_object(source)
        assert isinstance(ar, TentativelyAccept)

        assert ar.id == source["id"]

    def test_12_tentatively_reject(self):
        """Tentatively reject a notification."""
        ar = COARNotifyFactory.get_by_types(TentativelyReject.TYPE)
        assert ar == TentativelyReject

        source = TentativelyRejectFixtureFactory.source()
        ar = COARNotifyFactory.get_by_object(source)
        assert isinstance(ar, TentativelyReject)

        assert ar.id == source["id"]

    def test_13_unprocessable_notification(self):
        """Unprocessable notification."""
        ar = COARNotifyFactory.get_by_types(UnprocessableNotification.TYPE)
        assert ar == UnprocessableNotification

        source = UnprocessableNotificationFixtureFactory.source()
        ar = COARNotifyFactory.get_by_object(source)
        assert isinstance(ar, UnprocessableNotification)

        assert ar.id == source["id"]

    def test_14_undo_offer(self):
        """Undo an offer."""
        ar = COARNotifyFactory.get_by_types(UndoOffer.TYPE)
        assert ar == UndoOffer

        source = UndoOfferFixtureFactory.source()
        ar = COARNotifyFactory.get_by_object(source)
        assert isinstance(ar, UndoOffer)

        assert ar.id == source["id"]

    def test_15_register(self):
        """Register a new pattern."""

        class TestPattern(NotifyPattern):
            TYPE = Accept.TYPE

        COARNotifyFactory.register(TestPattern)

        tp = COARNotifyFactory.get_by_types(Accept.TYPE)
        assert tp == TestPattern
