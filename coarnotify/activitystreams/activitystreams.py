from coarnotify.constants import ConstantList

class Properties(ConstantList):
    ID = "id"
    TYPE = "type"
    ORIGIN = "origin"
    OBJECT = "object"
    TARGET = "target"
    ACTOR = "actor"
    IN_REPLY_TO = "inReplyTo"
    CONTEXT = "context"


class ActivityStream:
    DEFAULT = {
        "@context": "https://www.w3.org/ns/activitystreams"
    }

    def __init__(self, raw=None):
        self._raw = raw if raw is not None else {}
        self.add_jsonld_context(self.DEFAULT["@context"])

    @property
    def type(self):
        return self.get_property(Properties.TYPE)

    def add_jsonld_context(self, context):
        if "@context" not in self._raw:
            self._raw["@context"] = context
            return
        if self._raw["@context"] == context:
            return
        if not isinstance(self._raw["@context"], list):
            self._raw["@context"] = [self._raw["@context"]]
        if context not in self._raw["@context"]:
            self._raw["@context"].append(context)

    def set_property(self, prop_name, value):
        self._raw[prop_name] = value
        assert self._raw[prop_name] == value

    def get_property(self, prop_name):
        return self._raw.get(prop_name, None)

    def to_dict(self):
        return self._raw