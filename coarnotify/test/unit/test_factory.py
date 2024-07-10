from unittest import TestCase

from coarnotify.models.announce_endorsement import AnnounceEndorsement
from coarnotify.common import COARNotifyFactory

class TestFactory(TestCase):
    def test_01_announce_endorsement(self):
        ae = COARNotifyFactory.get("announce_endorsement")
        print(ae.to_dict())
        assert isinstance(ae, AnnounceEndorsement)
