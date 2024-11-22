from unittest import TestCase

from coarnotify.client import COARNotifyClient
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
    UndoOffer
)

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
    UndoOfferFixtureFactory
)

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

    def test_04_announce_relationship(self):
        client = COARNotifyClient(INBOX)
        source = AnnounceRelationshipFixtureFactory.source()
        ae = AnnounceRelationship(source)
        resp = client.send(ae)
        assert resp.action == resp.CREATED
        assert resp.location is not None
        print(resp.location)

    def test_05_announce_review(self):
        client = COARNotifyClient(INBOX)
        source = AnnounceReviewFixtureFactory.source()
        ae = AnnounceReview(source)
        resp = client.send(ae)
        assert resp.action == resp.CREATED
        assert resp.location is not None
        print(resp.location)

    def test_06_announce_service_result(self):
        client = COARNotifyClient(INBOX)
        source = AnnounceServiceResultFixtureFactory.source()
        ae = AnnounceServiceResult(source)
        resp = client.send(ae)
        assert resp.action == resp.CREATED
        assert resp.location is not None
        print(resp.location)

    def test_07_reject(self):
        client = COARNotifyClient(INBOX)
        source = RejectFixtureFactory.source()
        ae = Reject(source)
        resp = client.send(ae)
        assert resp.action == resp.CREATED
        assert resp.location is not None
        print(resp.location)

    def test_08_request_endorsement(self):
        client = COARNotifyClient(INBOX)
        source = RequestEndorsementFixtureFactory.source()
        ae = RequestEndorsement(source)
        resp = client.send(ae)
        assert resp.action == resp.CREATED
        assert resp.location is not None
        print(resp.location)

    def test_09_request_review(self):
        client = COARNotifyClient(INBOX)
        source = RequestReviewFixtureFactory.source()
        ae = RequestReview(source)
        resp = client.send(ae)
        assert resp.action == resp.CREATED
        assert resp.location is not None
        print(resp.location)

    def test_10_tentatively_accept(self):
        client = COARNotifyClient(INBOX)
        source = TentativelyAcceptFixtureFactory.source()
        ae = TentativelyAccept(source)
        resp = client.send(ae)
        assert resp.action == resp.CREATED
        assert resp.location is not None
        print(resp.location)

    def test_11_tentatively_reject(self):
        client = COARNotifyClient(INBOX)
        source = TentativelyRejectFixtureFactory.source()
        ae = TentativelyReject(source)
        resp = client.send(ae)
        assert resp.action == resp.CREATED
        assert resp.location is not None
        print(resp.location)

    def test_12_unprocessable_notification(self):
        client = COARNotifyClient(INBOX)
        source = UnprocessableNotificationFixtureFactory.source()
        ae = UnprocessableNotification(source)
        resp = client.send(ae)
        assert resp.action == resp.CREATED
        assert resp.location is not None
        print(resp.location)

    def test_13_undo_offer(self):
        client = COARNotifyClient(INBOX)
        source = UndoOfferFixtureFactory.source()
        ae = UndoOffer(source)
        resp = client.send(ae)
        assert resp.action == resp.CREATED
        assert resp.location is not None
        print(resp.location)
