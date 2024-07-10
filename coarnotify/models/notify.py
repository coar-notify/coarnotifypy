from coarnotify.activitystreams.activitystreams import ActivityStream, Properties
from coarnotify.constants import ConstantList
from typing import Union
import uuid
from copy import deepcopy

JSONLD_CONTEXT = "https://purl.org/coar/notify"


class NotifyProperties(ConstantList):
    INBOX = "inbox"


class Notify:
    DEFAULT_TYPE = "Object"
    ALLOWED_TYPES = []
    FORCE_TYPE = True

    def __init__(self, stream: Union[ActivityStream, dict] = None):
        if stream is None:
            self._stream = ActivityStream()
        elif isinstance(stream, dict):
            self._stream = ActivityStream(stream)
        else:
            self._stream = stream

        if self.FORCE_TYPE:
            self._stream.set_property(Properties.TYPE, self.DEFAULT_TYPE)
        if len(self.ALLOWED_TYPES) > 0:
            types = self._stream.get_property(Properties.TYPE)
            if types is not None:
                if not isinstance(types, list):
                    types = [types]
                if len(set(types).intersection(self.ALLOWED_TYPES)) != len(set(types)):
                    raise ValueError(f"Type value {types} is not one of the permitted values")

        if self._stream.get_property(Properties.ID) is None:
            self._stream.set_property(Properties.ID, "urn:uuid:" + str(uuid.uuid4().hex))


    @property
    def id(self):
        return self._stream.get_property(Properties.ID)

    @id.setter
    def id(self, value):
        self._stream.set_property(Properties.ID, value)

    @property
    def type(self):
        return self._stream.get_property(Properties.TYPE)

    @type.setter
    def type(self, value):
        types = value
        if not isinstance(value, list):
            types = [types]
        if len(self.ALLOWED_TYPES) > 0:
            if len(set(types).intersection(self.ALLOWED_TYPES)) != len(set(types)):
                raise ValueError("Type value is not one of the permitted values")
        self._stream.set_property(Properties.TYPE, value)

    @property
    def origin(self):
        o = self._stream.get_property(Properties.ORIGIN)
        if o is not None:
            return NotifyService(deepcopy(o))
        return None

    @origin.setter
    def origin(self, value: "NotifyService"):
        self._stream.set_property(Properties.ORIGIN, value.to_dict(include_jsonld_context=False))

    @property
    def target(self):
        t = self._stream.get_property(Properties.TARGET)
        if t is not None:
            return NotifyService(deepcopy(t))
        return None

    @target.setter
    def target(self, value: "NotifyService"):
        self._stream.set_property(Properties.TARGET, value.to_dict(include_jsonld_context=False))

    @property
    def object(self):
        o = self._stream.get_property(Properties.OBJECT)
        if o is not None:
            return NotifyObject(deepcopy(o))
        return None

    @object.setter
    def object(self, value: "NotifyObject"):
        self._stream.set_property(Properties.OBJECT, value.to_dict(include_jsonld_context=False))

    @property
    def in_reply_to(self):
        return self._stream.get_property(Properties.IN_REPLY_TO)

    @in_reply_to.setter
    def in_reply_to(self, value):
        self._stream.set_property(Properties.IN_REPLY_TO, value)

    @property
    def actor(self):
        a = self._stream.get_property(Properties.ACTOR)
        if a is not None:
            return NotifyActor(deepcopy(a))
        return None

    @actor.setter
    def actor(self, value: "NotifyActor"):
        self._stream.set_property(Properties.ACTOR, value.to_dict(include_jsonld_context=False))

    @property
    def context(self):
        c = self._stream.get_property(Properties.CONTEXT)
        if c is not None:
            return NotifyService(deepcopy(c))
        return None

    @context.setter
    def context(self, value: "NotifyContext"):
        self._stream.set_property(Properties.CONTEXT, value.to_dict(include_jsonld_context=False))

    def validate(self):
        return not (True in [
            self.id is None,
            self.type is None,
            self.origin is None,
            self.target is None#,
            # object is specified as required, but advised that this may be in error, so assuming not required for now
            #self.object is None
        ])

    def to_dict(self, include_jsonld_context=True):
        if include_jsonld_context:
            self._stream.add_jsonld_context(JSONLD_CONTEXT)
        d = self._stream.to_dict()
        if "@context" in d:
            del d["@context"]
        return d


class NotifyService(Notify):
    DEFAULT_TYPE = "Service"
    ALLOWED_TYPES = [DEFAULT_TYPE]

    def __init__(self, stream: Union[ActivityStream, dict] = None):
        super(NotifyService, self).__init__(stream=stream)

    @property
    def inbox(self):
        return self._stream.get_property(NotifyProperties.INBOX)

    @inbox.setter
    def inbox(self, value):
        self._stream.set_property(NotifyProperties.INBOX, value)


class NotifyObject(Notify):
    FORCE_TYPE = False

    def __init__(self, stream: Union[ActivityStream, dict] = None):
        super(NotifyObject, self).__init__(stream=stream)


class NotifyActor(Notify):
    DEFAULT_TYPE = "Service"
    ALLOWED_TYPES = [DEFAULT_TYPE]
    FORCE_TYPE = False

    def __init__(self, stream: Union[ActivityStream, dict] = None):
        super(NotifyActor, self).__init__(stream=stream)


class NotifyContext(Notify):
    FORCE_TYPE = False

    def __init__(self, stream: Union[ActivityStream, dict] = None):
        super(NotifyContext, self).__init__(stream=stream)