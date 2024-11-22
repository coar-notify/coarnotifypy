from unittest import TestCase
from copy import deepcopy

from coarnotify.exceptions import ValidationError

from coarnotify.core.notify import NotifyPattern, NotifyService, NotifyObject, NotifyActor, NotifyItem
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
from coarnotify.test.fixtures.notify import NotifyFixtureFactory
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


class TestModels(TestCase):

    def _get_testable_properties(self, source, prop_map=None):
        def expand(node, path):
            paths = []
            for k, v in node.items():
                if isinstance(v, dict):
                    paths += expand(v, f"{path}.{k}")
                else:
                    paths.append(f"{path}.{k}")
            paths = [p[1:] if p.startswith(".") else p for p in paths if "@context" not in p]  # strip the leading "."
            return paths

        obj_properties = expand(source, "")

        if prop_map is None:
            prop_map = {
                "inReplyTo": "in_reply_to",
                "context.ietf:cite-as": "context.cite_as",
                "context.ietf:item.id": "context.item.id",
                "context.ietf:item.mediaType": "context.item.media_type",
                "context.ietf:item.type": "context.item.type",
                "object.as:subject": "object.triple[2]",
                "object.as:relationship": "object.triple[1]",
                "object.as:object": "object.triple[0]",
                "object.ietf:cite-as": "object.cite_as",
                "object.ietf:item.id": "object.item.id",
                "object.ietf:item.mediaType": "object.item.media_type",
                "object.ietf:item.type": "object.item.type",
                "object.object.ietf:cite-as": "object.object.cite_as",
                "object.object.ietf:item.id": "object.object.item.id",
                "object.object.ietf:item.mediaType": "object.object.item.media_type",
                "object.object.ietf:item.type": "object.object.item.type",
            }

        proptest = [p if p not in prop_map else (prop_map[p], p) for p in obj_properties]
        return proptest

    def _apply_property_test(self, proptest, obj, fixtures):
        def get_prop(source, prop):
            p = prop
            if isinstance(prop, tuple):
                p = prop[1]
            bits = p.split(".")
            for bit in bits:
                idx = None
                if "[" in bit:
                    bit, idx = bit.split("[")
                    idx = int(idx[:-1])
                source = getattr(source, bit)
                if idx is not None:
                    source = source[idx]
            return source

        for prop in proptest:
            if isinstance(prop, tuple):
                oprop = prop[0]
                fprop = prop[1]
            else:
                oprop = prop
                fprop = prop

            print(oprop, fprop)
            oval = get_prop(obj, oprop)
            eval = fixtures.expected_value(fprop)

            # allow a single value to be equivalent to a list containing a single value
            if isinstance(oval, list) and len(oval) == 1:
                oval = oval[0]
            if isinstance(eval, list) and len(eval) == 1:
                eval = eval[0]

            assert oval == eval, f"{oprop}:{oval} - {fprop}:{eval}"

    def test_01_notify_manual_construct(self):
        n = NotifyPattern()

        # check the default properties
        assert n.id is not None
        assert n.id.startswith("urn:uuid:")
        assert n.type == NotifyPattern.TYPE
        assert n.origin is None
        assert n.target is None
        assert n.object is None
        assert n.actor is None
        assert n.in_reply_to is None
        assert n.context is None

        # now check the setters
        n.id = "urn:whatever"
        n.ALLOWED_TYPES = ["Object", "Other"]   # this is a hack to test the setter
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

        n.in_reply_to = "urn:irt"

        context = NotifyObject()
        assert context.id is not None
        assert context.type is None
        n.context = context

        assert n.id == "urn:whatever"
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
        assert n.in_reply_to == "urn:irt"
        assert n.context.id == context.id
        assert n.context.type is None

    def test_02_notify_from_fixture(self):
        source = NotifyFixtureFactory.source()
        n = NotifyPattern(source)

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
        n.id = "urn:whatever"
        n.ALLOWED_TYPES = ["Object", "Other"]  # this is a hack to test the setter
        n.type = "Other"
        assert n.id == "urn:whatever"
        assert n.type == "Other"

    def test_03_notify_operations(self):
        n = NotifyPattern()
        with self.assertRaises(ValidationError):
            n.validate()
        assert n.to_jsonld() is not None

        source = NotifyFixtureFactory.source()
        compare = deepcopy(source)
        n = NotifyPattern(source)
        assert n.validate() is True
        assert n.to_jsonld() == compare

    def test_04_accept(self):
        a = Accept()

        source = AcceptFixtureFactory.source()
        compare = deepcopy(source)
        a = Accept(source)
        assert a.validate() is True
        assert a.to_jsonld() == compare

        proptest = self._get_testable_properties(compare)
        self._apply_property_test(proptest, a, AcceptFixtureFactory)

    def test_05_announce_endorsement(self):
        ae = AnnounceEndorsement()
        source = AnnounceEndorsementFixtureFactory.source()
        compare = deepcopy(source)
        ae = AnnounceEndorsement(source)
        assert ae.validate() is True
        assert ae.to_jsonld() == compare

        proptest = self._get_testable_properties(compare)
        self._apply_property_test(proptest, ae, AnnounceEndorsementFixtureFactory)

    def test_07_announce_relationship(self):
        ae = AnnounceRelationship()

        source = AnnounceRelationshipFixtureFactory.source()
        compare = deepcopy(source)
        ae = AnnounceRelationship(source)
        assert ae.validate() is True
        assert ae.to_jsonld() == compare

        proptest = self._get_testable_properties(compare)
        self._apply_property_test(proptest, ae, AnnounceRelationshipFixtureFactory)

    def test_08_announce_review(self):
        ar = AnnounceReview()

        source = AnnounceReviewFixtureFactory.source()
        compare = deepcopy(source)
        ar = AnnounceReview(source)
        assert ar.validate() is True
        assert ar.to_jsonld() == compare

        proptest = self._get_testable_properties(compare)
        self._apply_property_test(proptest, ar, AnnounceReviewFixtureFactory)

    def test_09_announce_service_result(self):
        asr = AnnounceServiceResult()

        source = AnnounceServiceResultFixtureFactory.source()
        compare = deepcopy(source)
        compare["type"] = compare["type"][0]    # because it's a single field, but is a list in the fixture
        asr = AnnounceServiceResult(source)

        assert asr.validate() is True
        assert asr.to_jsonld() == compare

        proptest = self._get_testable_properties(compare)
        self._apply_property_test(proptest, asr, AnnounceServiceResultFixtureFactory)

    def test_10_reject(self):
        rej = Reject()

        source = RejectFixtureFactory.source()
        compare = deepcopy(source)
        rej = Reject(source)
        assert rej.validate() is True
        assert rej.to_jsonld() == compare

        proptest = self._get_testable_properties(compare)
        self._apply_property_test(proptest, rej, RejectFixtureFactory)

    def test_11_request_endorsement(self):
        re = RequestEndorsement()

        source = RequestEndorsementFixtureFactory.source()
        compare = deepcopy(source)
        re = RequestEndorsement(source)

        assert re.validate() is True
        assert re.to_jsonld() == compare

        proptest = self._get_testable_properties(compare)
        self._apply_property_test(proptest, re, RequestEndorsementFixtureFactory)

    def test_13_request_review(self):
        ri = RequestReview()

        source = RequestReviewFixtureFactory.source()
        compare = deepcopy(source)
        ri = RequestReview(source)

        assert ri.validate() is True
        assert ri.to_jsonld() == compare

        proptest = self._get_testable_properties(compare)
        self._apply_property_test(proptest, ri, RequestReviewFixtureFactory)

    def test_14_tentatively_accept(self):
        ta = TentativelyAccept()

        source = TentativelyAcceptFixtureFactory.source()
        compare = deepcopy(source)
        ta = TentativelyAccept(source)

        assert ta.validate() is True
        assert ta.to_jsonld() == compare

        proptest = self._get_testable_properties(compare)
        self._apply_property_test(proptest, ta, TentativelyAcceptFixtureFactory)

    def test_15_tentatively_reject(self):
        ta = TentativelyReject()

        source = TentativelyRejectFixtureFactory.source()
        compare = deepcopy(source)
        ta = TentativelyReject(source)

        assert ta.validate() is True
        assert ta.to_jsonld() == compare

        proptest = self._get_testable_properties(compare)
        self._apply_property_test(proptest, ta, TentativelyRejectFixtureFactory)

    def test_16_unprocessable_notification(self):
        ta = UnprocessableNotification()

        source = UnprocessableNotificationFixtureFactory.source()
        compare = deepcopy(source)
        ta = UnprocessableNotification(source)

        assert ta.validate() is True
        assert ta.to_jsonld() == compare

        proptest = self._get_testable_properties(compare)
        self._apply_property_test(proptest, ta, UnprocessableNotificationFixtureFactory)

    def test_17_undo_offer(self):
        ta = UndoOffer()

        source = UndoOfferFixtureFactory.source()
        compare = deepcopy(source)
        ta = UndoOffer(source)

        assert ta.validate() is True
        assert ta.to_jsonld() == compare

        proptest = self._get_testable_properties(compare)
        self._apply_property_test(proptest, ta, UndoOfferFixtureFactory)

    def test_18_by_ref(self):
        # Create a basic NotifyPatter, and explcitly declare properties by reference to be true (the default)
        n = NotifyPattern(properties_by_reference=True)

        # create an object externally, and confirm that it does not have a specific id
        obj = NotifyObject()
        assert obj.id != "urn:whatever"

        # assign the object to the pattern, then immediately retrieve it by the accessor, and set its
        # id.  We then confirm that both the original object and the pattern's version of the object are
        # *the same* object, and that the id is the same in both references
        n.object = obj
        n.object.id = "urn:whatever"
        assert n.object.id == "urn:whatever"
        assert obj.id == "urn:whatever"

        # Now we confirm that retrieving the record by reference also works.  Create a pattern,
        # and retrieve the object.  Set the ID of the object on the retrieved version, and confirm
        # that the original object also has the same ID (because they are the same, by reference)
        source = RequestReviewFixtureFactory.source()
        n = RequestReview(source, properties_by_reference=True)
        obj = n.object
        obj.id = "urn:whatever"
        assert n.object.id == "urn:whatever"

    def test_19_by_value(self):
        # Create a basic NotifyPatter, and explcitly declare properties by reference to be false.
        # Object should now be copied and passed around by value, so updates to one do not affect
        # the other
        n = NotifyPattern(properties_by_reference=False)

        # create an object externally, and confirm that it does not have a specific id
        obj = NotifyObject()
        assert obj.id != "urn:whatever"

        # assign the object to the pattern, then subsequently update its id.  Retrieve the object
        # from the pattern and confirm that the id change has not propagated
        n.object = obj
        obj.id = "urn:whatever"
        assert n.object.id != "urn:whatever"
        assert obj.id == "urn:whatever"

        # Same test again, but this time pull the object from the pattern first
        source = RequestReviewFixtureFactory.source()
        n = RequestReview(source, properties_by_reference=False)
        obj = n.object
        obj.id = "urn:whatever"
        assert n.object.id != "urn:whatever"

