from coarnotify.activitystreams2.activitystreams2 import ActivityStream, Properties
from coarnotify.constants import ConstantList
from coarnotify import validate
from coarnotify.exceptions import ValidationError
from typing import Union
import uuid
from copy import deepcopy

NOTIFY_NAMESPACE = "https://purl.org/coar/notify"


class NotifyProperties(ConstantList):
    INBOX = ("inbox", NOTIFY_NAMESPACE)


class NotifyBase:
    def __init__(self, stream: Union[ActivityStream, dict] = None):
        if stream is None:
            self._stream = ActivityStream()
        elif isinstance(stream, dict):
            self._stream = ActivityStream(stream)
        else:
            self._stream = stream

        if self._stream.get_property(Properties.ID) is None:
            self._stream.set_property(Properties.ID, "urn:uuid:" + str(uuid.uuid4().hex))

    @property
    def doc(self):
        return self._stream.doc

    @property
    def id(self) -> str:
        return self._stream.get_property(Properties.ID)

    @id.setter
    def id(self, value: str):
        self._stream.set_property(Properties.ID, value)

    @property
    def type(self) -> Union[str, list[str]]:
        return self._stream.get_property(Properties.TYPE)

    @type.setter
    def type(self, types: Union[str, list[str]]):
        self._stream.set_property(Properties.TYPE, types)

    def validate(self):
        ve = ValidationError()
        if self.id is None:
            ve.add_error(Properties.ID, validate.REQUIRED_MESSAGE.format(x=Properties.ID[0]))
        if self.type is None:
            ve.add_error(Properties.TYPE, validate.REQUIRED_MESSAGE.format(x=Properties.TYPE[0]))
        if ve.has_errors():
            raise ve
        return True

    def to_jsonld(self):
        return self._stream.to_jsonld()


class NotifyDocument(NotifyBase):
    TYPE = "Object"

    def __init__(self, stream: Union[ActivityStream, dict] = None):
        super(NotifyDocument, self).__init__(stream=stream)
        self._ensure_type_contains(self.TYPE)

    def _ensure_type_contains(self, types: Union[str, list[str]]):
        existing = self._stream.get_property(Properties.TYPE)
        if existing is None:
            self._stream.set_property(Properties.TYPE, types)
        else:
            if not isinstance(existing, list):
                existing = [existing]
            if not isinstance(types, list):
                types = [types]
            for t in types:
                if t not in existing:
                    existing.append(t)
            if len(existing) == 1:
                existing = existing[0]
            self._stream.set_property(Properties.TYPE, existing)

    @property
    def origin(self) -> Union["NotifyService", None]:
        o = self._stream.get_property(Properties.ORIGIN)
        if o is not None:
            return NotifyService(deepcopy(o))
        return None

    @origin.setter
    def origin(self, value: "NotifyService"):
        self._stream.set_property(Properties.ORIGIN, value.doc)

    @property
    def target(self) -> Union["NotifyService", None]:
        t = self._stream.get_property(Properties.TARGET)
        if t is not None:
            return NotifyService(deepcopy(t))
        return None

    @target.setter
    def target(self, value: "NotifyService"):
        self._stream.set_property(Properties.TARGET, value.doc)

    @property
    def object(self) -> Union["NotifyObject", None]:
        o = self._stream.get_property(Properties.OBJECT)
        if o is not None:
            return NotifyObject(deepcopy(o))
        return None

    @object.setter
    def object(self, value: "NotifyObject"):
        self._stream.set_property(Properties.OBJECT, value.doc)

    @property
    def in_reply_to(self) -> str:
        return self._stream.get_property(Properties.IN_REPLY_TO)

    @in_reply_to.setter
    def in_reply_to(self, value: str):
        self._stream.set_property(Properties.IN_REPLY_TO, value)

    @property
    def actor(self) -> Union["NotifyActor", None]:
        a = self._stream.get_property(Properties.ACTOR)
        if a is not None:
            return NotifyActor(deepcopy(a))
        return None

    @actor.setter
    def actor(self, value: "NotifyActor"):
        self._stream.set_property(Properties.ACTOR, value.doc)

    @property
    def context(self) -> Union["NotifyObject", None]:
        c = self._stream.get_property(Properties.CONTEXT)
        if c is not None:
            return NotifyObject(deepcopy(c))
        return None

    @context.setter
    def context(self, value: "NotifyObject"):
        self._stream.set_property(Properties.CONTEXT, value.doc)

    def validate(self):
        ve = ValidationError()
        try:
            super(NotifyDocument, self).validate()
        except ValidationError as superve:
            ve = superve

        if self.origin is None:
            ve.add_error(Properties.ORIGIN, validate.REQUIRED_MESSAGE.format(x=Properties.ORIGIN[0]))
        else:
            try:
                self.origin.validate()
            except ValidationError as subve:
                ve.add_nested_errors(Properties.ORIGIN, subve)

        if self.target is None:
            ve.add_error(Properties.TARGET, validate.REQUIRED_MESSAGE.format(x=Properties.TARGET[0]))
        else:
            try:
                self.target.validate()
            except ValidationError as subve:
                ve.add_nested_errors(Properties.TARGET, subve)

        if self.object is None:
            ve.add_error(Properties.OBJECT, validate.REQUIRED_MESSAGE.format(x=Properties.OBJECT[0]))
        else:
            try:
                self.object.validate()
            except ValidationError as subve:
                ve.add_nested_errors(Properties.OBJECT, subve)

        if ve.has_errors():
            raise ve

        return True


class NotifyDocumentPart(NotifyBase):
    DEFAULT_TYPE = None
    ALLOWED_TYPES = []

    def __init__(self, stream: Union[ActivityStream, dict] = None):
        super(NotifyDocumentPart, self).__init__(stream=stream)
        if self.DEFAULT_TYPE is not None and self.type is None:
            self.type = self.DEFAULT_TYPE

    @NotifyBase.type.setter
    def type(self, types: Union[str, list[str]]):

        if not isinstance(types, list):
            types = [types]

        if len(self.ALLOWED_TYPES) > 0:
            for t in types:
                if t not in self.ALLOWED_TYPES:
                    raise ValueError(f"Type value {t} is not one of the permitted values")

        # keep single values as single values, not lists
        if len(types) == 1:
            types = types[0]

        self._stream.set_property(Properties.TYPE, types)

    def to_dict(self):
        return self._stream.doc


class NotifyService(NotifyDocumentPart):
    DEFAULT_TYPE = "Service"
    ALLOWED_TYPES = [DEFAULT_TYPE]

    def __init__(self, stream: Union[ActivityStream, dict] = None):
        super(NotifyService, self).__init__(stream=stream)

    @property
    def inbox(self) -> str:
        return self._stream.get_property(NotifyProperties.INBOX)

    @inbox.setter
    def inbox(self, value: str):
        self._stream.set_property(NotifyProperties.INBOX, value)

    def validate(self):
        ve = ValidationError()
        try:
            super(NotifyService, self).validate()
        except ValidationError as superve:
            ve = superve

        if self.inbox is None:
            ve.add_error(NotifyProperties.INBOX, validate.REQUIRED_MESSAGE.format(x=NotifyProperties.INBOX[0]))

        if ve.has_errors():
            raise ve

        return True


class NotifyObject(NotifyDocumentPart):

    def __init__(self, stream: Union[ActivityStream, dict] = None):
        super(NotifyObject, self).__init__(stream=stream)

    @property
    def cite_as(self) -> str:
        return self._stream.get_property("ietf:cite-as")

    @cite_as.setter
    def cite_as(self, value: str):
        self._stream.set_property("ietf:cite-as", value)

    @property
    def item(self) -> Union["NotifyItem", None]:
        i = self._stream.get_property("ietf:item")
        if i is not None:
            return NotifyItem(deepcopy(i))
        return None

    @item.setter
    def item(self, value: "NotifyItem"):
        self._stream.set_property("ietf:item", value)

    @property
    def triple(self) -> tuple[str, str, str]:
        obj = self._stream.get_property("as:object")
        rel = self._stream.get_property("as:relationship")
        subj = self._stream.get_property("as:subject")
        return obj, rel, subj

    @triple.setter
    def triple(self, value: tuple[str, str, str]):
        obj, rel, subj = value
        self._stream.set_property("as:object", obj)
        self._stream.set_property("as:relationship", rel)
        self._stream.set_property("as:subject", subj)


class NotifyActor(NotifyDocumentPart):
    DEFAULT_TYPE = "Service"
    ALLOWED_TYPES = [DEFAULT_TYPE, "Application", "Group", "Organization", "Person"]

    def __init__(self, stream: Union[ActivityStream, dict] = None):
        super(NotifyActor, self).__init__(stream=stream)

    @property
    def name(self) -> str:
        return self._stream.get_property("name")

    @name.setter
    def name(self, value: str):
        self._stream.set_property("name", value)


class NotifyItem(NotifyDocumentPart):

    def __init__(self, stream: Union[ActivityStream, dict] = None):
        super(NotifyItem, self).__init__(stream=stream)

    @property
    def media_type(self) -> str:
        return self._stream.get_property("mediaType")

    @media_type.setter
    def media_type(self, value: str):
        self._stream.set_property("mediaType", value)
