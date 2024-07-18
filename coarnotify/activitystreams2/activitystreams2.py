from coarnotify.constants import ConstantList
from typing import Union


ACTIVITY_STREAMS_NAMESPACE = "https://www.w3.org/ns/activitystreams"


class Properties(ConstantList):
    ID = ("id", ACTIVITY_STREAMS_NAMESPACE)
    TYPE = ("type", ACTIVITY_STREAMS_NAMESPACE)
    ORIGIN = ("origin", ACTIVITY_STREAMS_NAMESPACE)
    OBJECT = ("object", ACTIVITY_STREAMS_NAMESPACE)
    TARGET = ("target", ACTIVITY_STREAMS_NAMESPACE)
    ACTOR = ("actor", ACTIVITY_STREAMS_NAMESPACE)
    IN_REPLY_TO = ("inReplyTo", ACTIVITY_STREAMS_NAMESPACE)
    CONTEXT = ("context", ACTIVITY_STREAMS_NAMESPACE)
    SUMMARY = ("summary", ACTIVITY_STREAMS_NAMESPACE)


class ActivityStream:
    def __init__(self, raw=None):
        self._doc = raw if raw is not None else {}
        self._context = []
        if "@context" in self._doc:
            self._context = self._doc["@context"]
            if not isinstance(self._context, list):
                self._context = [self._context]
            del self._doc["@context"]

    @property
    def doc(self):
        return self._doc

    @doc.setter
    def doc(self, doc):
        self._doc = doc

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, context):
        self._context = context

    def _register_namespace(self, namespace: Union[str, tuple[str, str]]):
        entry = namespace
        if isinstance(namespace, tuple):
            url = namespace[1]
            short = namespace[0]
            entry = {short: url}

        if entry not in self._context:
            self._context.append(entry)

    def set_property(self, property: Union[str, tuple[str, str], tuple[str, tuple[str, str]]], value):
        prop_name = property
        namespace = None
        if isinstance(property, tuple):
            prop_name = property[0]
            namespace = property[1]

        self._doc[prop_name] = value
        if namespace is not None:
            self._register_namespace(namespace)

    def get_property(self, property: Union[str, tuple[str, str], tuple[str, tuple[str, str]]]):
        prop_name = property
        namespace = None
        if isinstance(property, tuple):
            prop_name = property[0]
            namespace = property[1]

        return self._doc.get(prop_name, None)

    def to_jsonld(self):
        return {
            "@context": self._context,
            **self._doc
        }