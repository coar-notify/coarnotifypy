from unittest import TestCase
from copy import deepcopy

from coarnotify.exceptions import ValidationError

from coarnotify.models import NotifyDocument, NotifyService, NotifyObject, NotifyActor, NotifyItem
from coarnotify.models import (
    Accept,
    AnnounceEndorsement,
    AnnounceIngest,
    AnnounceRelationship,
    AnnounceReview,
    AnnounceServiceResult,
    Reject,
    RequestEndorsement,
    RequestIngest
)
from coarnotify.test.fixtures.notify import NotifyFixtureFactory
from coarnotify.test.fixtures import (
    AcceptFixtureFactory,
    AnnounceEndorsementFixtureFactory,
    AnnounceIngestFixtureFactory,
    AnnounceRelationshipFixtureFactory,
    AnnounceReviewFixtureFactory,
    AnnounceServiceResultFixtureFactory,
    RejectFixtureFactory,
    RequestEndorsementFixtureFactory,
    RequestIngestFixtureFactory
)


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
        n.id = "urn:whatever"
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
        n.id = "urn:whatever"
        n.type = "Other"
        assert n.id == "urn:whatever"
        assert n.type == "Other"

    def test_03_notify_operations(self):
        n = NotifyDocument()
        with self.assertRaises(ValidationError):
            n.validate()
        assert n.to_jsonld() is not None

        source = NotifyFixtureFactory.source()
        compare = deepcopy(source)
        n = NotifyDocument(source)
        assert n.validate() is True
        assert n.to_jsonld() == compare

    def test_04_accept(self):
        a = Accept()

        source = AcceptFixtureFactory.source()
        compare = deepcopy(source)
        a = Accept(source)
        assert a.validate() is True
        assert a.to_jsonld() == compare

        assert a.id == "urn:uuid:4fb3af44-d4f8-4226-9475-2d09c2d8d9e0"
        assert a.in_reply_to == "urn:uuid:0370c0fb-bb78-4a9b-87f5-bed307a509dd"

        assert a.origin.id == "https://generic-service.com/system"
        assert a.origin.inbox == "https://generic-service.com/system/inbox/"
        assert a.origin.type == "Service"

        assert a.object.id == "urn:uuid:4fb3af44-1111-4226-9475-2d09c2d8d9e0"
        assert a.object.type == "Offer"

        assert a.target.id == "https://some-organisation.org"
        assert a.target.inbox == "https://some-organisation.org/inbox/"
        assert a.target.type == "Organization"

        assert a.type == "Accept"

    def test_05_announce_endorsement(self):
        ae = AnnounceEndorsement()
        source = AnnounceEndorsementFixtureFactory.source()
        compare = deepcopy(source)
        ae = AnnounceEndorsement(source)
        assert ae.validate() is True
        assert ae.to_jsonld() == compare

        assert ae.id == "urn:uuid:94ecae35-dcfd-4182-8550-22c7164fe23f"
        assert ae.type == ["Announce", "coar-notify:EndorsementAction"]

        assert ae.origin.id == "https://overlay-journal.com/system"
        assert ae.origin.inbox == "https://overlay-journal.com/inbox/"
        assert ae.origin.type == "Service"

        assert ae.object.id == "https://overlay-journal.com/articles/00001/"
        assert ae.object.cite_as == "https://overlay-journal.com/articles/00001/"
        assert ae.object.type == ["Page", "sorg:WebPage"]

        assert ae.target.id == "https://research-organisation.org/repository"
        assert ae.target.inbox == "https://research-organisation.org/inbox/"
        assert ae.target.type == "Service"

        assert ae.actor.id == "https://overlay-journal.com"
        assert ae.actor.name == "Overlay Journal"
        assert ae.actor.type == "Service"

        assert ae.in_reply_to == "urn:uuid:0370c0fb-bb78-4a9b-87f5-bed307a509dd"
        assert ae.context.id == "https://research-organisation.org/repository/preprint/201203/421/"
        assert ae.context.cite_as == "https://doi.org/10.5555/12345680"
        assert ae.context.type == "sorg:AboutPage"

        item = ae.context.item
        assert item.id == "https://research-organisation.org/repository/preprint/201203/421/content.pdf"
        assert item.media_type == "application/pdf"
        assert item.type == ["Article", "sorg:ScholarlyArticle"]

    def test_06_announce_ingest(self):
        ai = AnnounceIngest()

        source = AnnounceIngestFixtureFactory.source()
        compare = deepcopy(source)
        ai = AnnounceIngest(source)
        assert ai.validate() is True
        assert ai.to_jsonld() == compare

        assert ai.actor.id == "https://research-organisation.org"
        assert ai.actor.name == "Research Organisation"
        assert ai.actor.type == "Organization"

        assert ai.context.id == "https://research-organisation.org/repository/preprint/201203/421/"
        assert ai.context.cite_as == "https://doi.org/10.5555/12345680"
        assert ai.context.type == "sorg:AboutPage"
        item = ai.context.item
        assert item.id == "https://research-organisation.org/repository/preprint/201203/421/content.pdf"
        assert item.media_type == "application/pdf"
        assert item.type == ["Article", "sorg:ScholarlyArticle"]

        assert ai.id == "urn:uuid:94ecae35-dcfd-4182-8550-22c7164fe23f"
        assert ai.in_reply_to == "urn:uuid:0370c0fb-bb78-4a9b-87f5-bed307a509dd"

        assert ai.object.id == "https://research-organisation.org/repository/preprint/201203/421/"
        assert ai.object.cite_as == "https://doi.org/10.5555/12345680"
        item = ai.object.item
        assert item.id == "https://research-organisation.org/repository/preprint/201203/421/content.pdf"
        assert item.media_type == "application/pdf"
        assert item.type == ["Article", "sorg:ScholarlyArticle"]

        assert ai.origin.id == "https://research-organisation.org/repository"
        assert ai.origin.inbox == "https://research-organisation.org/inbox/"
        assert ai.origin.type == "Service"

        assert ai.target.id == "https://overlay-journal.com/system"
        assert ai.target.inbox == "https://overlay-journal.com/inbox/"
        assert ai.target.type == "Service"

        assert ai.type == ["Announce", "coar-notify:IngestAction"]

    def test_07_announce_relationship(self):
        ae = AnnounceRelationship()

        source = AnnounceRelationshipFixtureFactory.source()
        compare = deepcopy(source)
        ae = AnnounceRelationship(source)
        assert ae.validate() is True
        assert ae.to_jsonld() == compare

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

    def test_08_announce_review(self):
        ar = AnnounceReview()

        source = AnnounceReviewFixtureFactory.source()
        compare = deepcopy(source)
        ar = AnnounceReview(source)
        assert ar.validate() is True
        assert ar.to_jsonld() == compare

        # now test we are properly reading the fixture
        assert ar.actor.id == "https://review-service.com"
        assert ar.actor.name == "Review Service"
        assert ar.actor.type == "Service"

        assert ar.context.id == "https://research-organisation.org/repository/preprint/201203/421/"
        assert ar.context.cite_as == "https://doi.org/10.5555/12345680"
        assert ar.context.type == "sorg:AboutPage"
        item = ar.context.item
        assert item.id == "https://research-organisation.org/repository/preprint/201203/421/content.pdf"
        assert item.media_type == "application/pdf"
        assert item.type == ["Article", "sorg:ScholarlyArticle"]

        assert ar.id == "urn:uuid:94ecae35-dcfd-4182-8550-22c7164fe23f"
        assert ar.in_reply_to == "urn:uuid:0370c0fb-bb78-4a9b-87f5-bed307a509dd"

        assert ar.object.id == "https://review-service.com/review/geo/202103/0021"
        assert ar.object.cite_as == "https://doi.org/10.3214/987654"
        assert ar.object.type == ["Document", "sorg:Review"]

        assert ar.origin.id == "https://review-service.com/system"
        assert ar.origin.inbox == "https://review-service.com/inbox/"
        assert ar.origin.type == "Service"

        assert ar.target.id == "https://generic-service.com/system"
        assert ar.target.inbox == "https://generic-service.com/system/inbox/"
        assert ar.target.type == "Service"

        assert ar.type == ["Announce", "coar-notify:ReviewAction"]

    def test_09_announce_service_result(self):
        asr = AnnounceServiceResult()

        source = AnnounceServiceResultFixtureFactory.source()
        compare = deepcopy(source)
        asr = AnnounceServiceResult(source)
        assert asr.validate() is True
        assert asr.to_jsonld() == compare

        # now test we are properly reading the fixture
        assert asr.actor.id == "https://overlay-journal.com"
        assert asr.actor.name == "Overlay Journal"
        assert asr.actor.type == "Service"

        assert asr.context.id == "https://research-organisation.org/repository/preprint/201203/421/"
        assert asr.context.cite_as == "https://doi.org/10.5555/12345680"
        assert asr.context.type == "sorg:AboutPage"

        item = asr.context.item
        assert item.id == "https://research-organisation.org/repository/preprint/201203/421/content.pdf"
        assert item.media_type == "application/pdf"
        assert item.type == ["Article", "sorg:ScholarlyArticle"]

        assert asr.id == "urn:uuid:94ecae35-dcfd-4182-8550-22c7164fe23f"
        assert asr.in_reply_to == "urn:uuid:0370c0fb-bb78-4a9b-87f5-bed307a509dd"

        assert asr.object.id == "https://overlay-journal.com/information-page"
        assert asr.object.type == ["Page", "sorg:WebPage"]

        assert asr.origin.id == "https://overlay-journal.com/system"
        assert asr.origin.inbox == "https://overlay-journal.com/inbox/"
        assert asr.origin.type == "Service"

        assert asr.target.id == "https://generic-service.com/system"
        assert asr.target.inbox == "https://generic-service.com/system/inbox/"
        assert asr.target.type == "Service"

        assert asr.type == "Announce"

    def test_10_reject(self):
        rej = Reject()

        source = RejectFixtureFactory.source()
        compare = deepcopy(source)
        rej = Reject(source)
        assert rej.validate() is True
        assert rej.to_jsonld() == compare

        # now test we are properly reading the fixture
        assert rej.id == "urn:uuid:668f26e0-2c8d-4117-a0d2-ee713523bcb1"
        assert rej.in_reply_to == "urn:uuid:0370c0fb-bb78-4a9b-87f5-bed307a509dd"

        assert rej.origin.id == "https://generic-service.com/system"
        assert rej.origin.inbox == "https://generic-service.com/system/inbox/"
        assert rej.origin.type == "Service"

        assert rej.target.id == "https://some-organisation.org"
        assert rej.target.inbox == "https://some-organisation.org/inbox/"
        assert rej.target.type == "Organization"

        assert rej.type == "Reject"

    def test_11_request_endorsement(self):
        re = RequestEndorsement()

        source = RequestEndorsementFixtureFactory.source()
        compare = deepcopy(source)
        re = RequestEndorsement(source)
        assert re.validate() is True
        assert re.to_jsonld() == compare

        assert re.actor.id == "https://orcid.org/0000-0002-1825-0097"
        assert re.actor.name == "Josiah Carberry"
        assert re.actor.type == "Person"

        assert re.id == "urn:uuid:0370c0fb-bb78-4a9b-87f5-bed307a509dd"
        assert re.object.id == "https://research-organisation.org/repository/preprint/201203/421/"
        assert re.object.cite_as == "https://doi.org/10.5555/12345680"
        item = re.object.item
        assert item.id == "https://research-organisation.org/repository/preprint/201203/421/content.pdf"
        assert item.media_type == "application/pdf"
        assert item.type == ["Article", "sorg:ScholarlyArticle"]
        assert re.object.type == "sorg:AboutPage"

        assert re.origin.id == "https://research-organisation.org/repository"
        assert re.origin.inbox == "https://research-organisation.org/inbox/"
        assert re.origin.type == "Service"

        assert re.target.id == "https://overlay-journal.com/system"
        assert re.target.inbox == "https://overlay-journal.com/inbox/"
        assert re.target.type == "Service"

        assert re.type == ["Offer", "coar-notify:EndorsementAction"]

    def test_12_request_ingest(self):
        ri = RequestIngest()

        source = RequestIngestFixtureFactory.source()
        compare = deepcopy(source)
        ri = RequestIngest(source)

        assert ri.validate() is True
        assert ri.to_jsonld() == compare

        assert ri.actor.id == "https://overlay-journal.com"
        assert ri.actor.name == "Overlay Journal"
        assert ri.actor.type == "Service"

        assert ri.id == "urn:uuid:0370c0fb-bb78-4a9b-87f5-bed307a509dd"

        obj = ri.object
        assert obj.id == "https://research-organisation.org/repository/preprint/201203/421/"
        assert obj.cite_as == "https://doi.org/10.5555/12345680"
        assert obj.type == "sorg:AboutPage"
        assert obj.item.id == "https://research-organisation.org/repository/preprint/201203/421/content.pdf"
        assert obj.item.media_type == "application/pdf"
        assert obj.item.type == ["Article", "sorg:ScholarlyArticle"]

        assert ri.origin.id == "https://overlay-journal.com/system"
        assert ri.origin.inbox == "https://overlay-journal.com/inbox/"
        assert ri.origin.type == "Service"

        assert ri.target.id == "https://research-organisation.org/repository"
        assert ri.target.inbox == "https://research-organisation.org/inbox/"
        assert ri.target.type == "Service"

