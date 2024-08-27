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
    CITE_AS = ("ietf:cite-as", NOTIFY_NAMESPACE)
    ITEM = ("ietf:item", NOTIFY_NAMESPACE)


VALIDATION_RULES = {
    Properties.ID: {
        "default": validate.absolute_uri,
        "context": {
            # In some places this is a URI and in others an HTTP URI - unclear of the requirement
            # Properties.OBJECT: {
            #     "default": validate.url     # For AnnounceEndorsement, AnnounceServiceResult this is not specified clearly, AnnounceRelationship says URI
            # },
            Properties.CONTEXT: {
                "default": validate.url
            },
            Properties.ORIGIN: {
                "default": validate.url
            },
            Properties.TARGET: {
                "default": validate.url
            },
            NotifyProperties.ITEM: {
                "default": validate.url
            }
        }
    },
    Properties.TYPE: {
        "default": None,
        "context": {
            Properties.ACTOR: {
                "default": validate.one_of(["Service", "Application", "Group", "Organization", "Person"])   # is this a MUST or a SHOULD?
            },
            Properties.OBJECT: {
                "default": validate.contains("sorg:AboutPage"),
            },
            Properties.ORIGIN: {
                "default": validate.contains("Service")
            },
            Properties.TARGET: {
                "default": validate.contains("Service")
            },
            Properties.CONTEXT: {
                "default": validate.contains("sorg:AboutPage")
            }
        }
    },
    NotifyProperties.CITE_AS: {
        "default": validate.url
    },
    NotifyProperties.INBOX: {
        "default": validate.url
    },
    Properties.IN_REPLY_TO: {
        "default": validate.absolute_uri
    },
    Properties.SUBJECT_TRIPLE: {
        "default": validate.absolute_uri
    },
    Properties.OBJECT_TRIPLE: {
        "default": validate.absolute_uri
    },
    Properties.RELATIONSHIP_TRIPLE: {
        "default": validate.absolute_uri
    }
}

VALIDATORS = validate.Validator(VALIDATION_RULES)


class NotifyBase:
    def __init__(self, stream: Union[ActivityStream, dict] = None,
                 validate_stream_on_construct=True,
                 validate_properties=True,
                 validators=None,
                 validation_context=None):
        self._validate_stream_on_construct = validate_stream_on_construct
        self._validate_properties = validate_properties
        self._validators = validators if validators is not None else VALIDATORS
        self._validation_context = validation_context
        validate_now = False

        if stream is None:
            self._stream = ActivityStream()
        elif isinstance(stream, dict):
            validate_now = validate_stream_on_construct
            self._stream = ActivityStream(stream)
        else:
            validate_now = validate_stream_on_construct
            self._stream = stream

        if self._stream.get_property(Properties.ID) is None:
            self._stream.set_property(Properties.ID, "urn:uuid:" + str(uuid.uuid4().hex))

        if validate_now:
            self.validate()

    @property
    def validate_properties(self):
        return self._validate_properties

    @property
    def validate_stream_on_construct(self):
        return self._validate_stream_on_construct

    @property
    def validators(self):
        return self._validators

    @property
    def doc(self):
        return self._stream.doc

    @property
    def id(self) -> str:
        return self.get_property(Properties.ID)

    @id.setter
    def id(self, value: str):
        self.set_property(Properties.ID, value)

    @property
    def type(self) -> Union[str, list[str]]:
        return self.get_property(Properties.TYPE)

    @type.setter
    def type(self, types: Union[str, list[str]]):
        self.set_property(Properties.TYPE, types)

    def get_property(self, prop_name):
        return self._stream.get_property(prop_name)

    def set_property(self, prop_name, value):
        self.validate_property(prop_name, value)
        self._stream.set_property(prop_name, value)

    def validate(self):
        ve = ValidationError()
        if self.id is None:
            ve.add_error(Properties.ID, validate.REQUIRED_MESSAGE.format(x=Properties.ID[0]))
        else:
            self.register_property_validation_error(ve, Properties.ID, self.id)

        if self.type is None:
            ve.add_error(Properties.TYPE, validate.REQUIRED_MESSAGE.format(x=Properties.TYPE[0]))
        else:
            self.register_property_validation_error(ve, Properties.TYPE, self.type)

        if ve.has_errors():
            raise ve
        return True

    def validate_property(self, prop_name: str, value, force_validate=False, raise_error=True):
        if value is None:
            return True, ""
        if self.validate_properties or force_validate:
            validator = self.validators.get(prop_name, self._validation_context)
            if validator is not None:
                try:
                    validator(value)
                except ValueError as ve:
                    if raise_error:
                        raise ve
                    else:
                        return False, str(ve)
        return True, ""

    def register_property_validation_error(self, ve: ValidationError, prop_name: str, value):
        e, msg = self.validate_property(prop_name, value, force_validate=True, raise_error=False)
        if not e:
            ve.add_error(prop_name, msg)

    def to_jsonld(self):
        return self._stream.to_jsonld()


class NotifyDocument(NotifyBase):
    TYPE = "Object"

    def __init__(self, stream: Union[ActivityStream, dict] = None,
                 validate_stream_on_construct=True,
                 validate_properties=True,
                 validators=None,
                 validation_context=None):
        super(NotifyDocument, self).__init__(stream=stream,
                                             validate_stream_on_construct=validate_stream_on_construct,
                                             validate_properties=validate_properties,
                                             validators=validators,
                                             validation_context=validation_context)
        self._ensure_type_contains(self.TYPE)

    def _ensure_type_contains(self, types: Union[str, list[str]]):
        existing = self._stream.get_property(Properties.TYPE)
        if existing is None:
            self.set_property(Properties.TYPE, types)
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
            self.set_property(Properties.TYPE, existing)

    @property
    def origin(self) -> Union["NotifyService", None]:
        o = self.get_property(Properties.ORIGIN)
        if o is not None:
            return NotifyService(deepcopy(o),
                                 validate_stream_on_construct=False,
                                 validate_properties=self.validate_properties,
                                 validators=self.validators,
                                 validation_context=Properties.ORIGIN)
        return None

    @origin.setter
    def origin(self, value: "NotifyService"):
        self.set_property(Properties.ORIGIN, value.doc)

    @property
    def target(self) -> Union["NotifyService", None]:
        t = self.get_property(Properties.TARGET)
        if t is not None:
            return NotifyService(deepcopy(t),
                                 validate_stream_on_construct=False,
                                 validate_properties=self.validate_properties,
                                 validators=self.validators,
                                 validation_context=Properties.TARGET)
        return None

    @target.setter
    def target(self, value: "NotifyService"):
        self.set_property(Properties.TARGET, value.doc)

    @property
    def object(self) -> Union["NotifyObject", None]:
        o = self.get_property(Properties.OBJECT)
        if o is not None:
            return NotifyObject(deepcopy(o),
                                 validate_stream_on_construct=False,
                                 validate_properties=self.validate_properties,
                                 validators=self.validators,
                                 validation_context=Properties.OBJECT)
        return None

    @object.setter
    def object(self, value: "NotifyObject"):
        self.set_property(Properties.OBJECT, value.doc)

    @property
    def in_reply_to(self) -> str:
        return self.get_property(Properties.IN_REPLY_TO)

    @in_reply_to.setter
    def in_reply_to(self, value: str):
        self.set_property(Properties.IN_REPLY_TO, value)

    @property
    def actor(self) -> Union["NotifyActor", None]:
        a = self.get_property(Properties.ACTOR)
        if a is not None:
            return NotifyActor(deepcopy(a),
                                 validate_stream_on_construct=False,
                                 validate_properties=self.validate_properties,
                                 validators=self.validators,
                                 validation_context=Properties.ACTOR)
        return None

    @actor.setter
    def actor(self, value: "NotifyActor"):
        self.set_property(Properties.ACTOR, value.doc)

    @property
    def context(self) -> Union["NotifyObject", None]:
        c = self.get_property(Properties.CONTEXT)
        if c is not None:
            return NotifyObject(deepcopy(c),
                                 validate_stream_on_construct=False,
                                 validate_properties=self.validate_properties,
                                 validators=self.validators,
                                 validation_context=Properties.CONTEXT)
        return None

    @context.setter
    def context(self, value: "NotifyObject"):
        self.set_property(Properties.CONTEXT, value.doc)

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

        if self.actor is not None:
            try:
                self.actor.validate()
            except ValidationError as subve:
                ve.add_nested_errors(Properties.ACTOR, subve)

        if self.in_reply_to is not None:
            self.register_property_validation_error(ve, Properties.IN_REPLY_TO, self.in_reply_to)

        if self.context is not None:
            try:
                self.context.validate()
            except ValidationError as subve:
                ve.add_nested_errors(Properties.CONTEXT, subve)

        if ve.has_errors():
            raise ve

        return True


class NotifyDocumentPart(NotifyBase):
    DEFAULT_TYPE = None
    ALLOWED_TYPES = []

    def __init__(self, stream: Union[ActivityStream, dict] = None,
                 validate_stream_on_construct=True,
                 validate_properties=True,
                 validators=None,
                 validation_context=None):
        super(NotifyDocumentPart, self).__init__(stream=stream,
                                                 validate_stream_on_construct=validate_stream_on_construct,
                                                 validate_properties=validate_properties,
                                                 validators=validators,
                                                 validation_context=validation_context)
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

        self.set_property(Properties.TYPE, types)

    def to_dict(self):
        return self._stream.doc


class NotifyService(NotifyDocumentPart):
    DEFAULT_TYPE = "Service"
    ALLOWED_TYPES = [DEFAULT_TYPE]

    @property
    def inbox(self) -> str:
        return self.get_property(NotifyProperties.INBOX)

    @inbox.setter
    def inbox(self, value: str):
        self.set_property(NotifyProperties.INBOX, value)

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

    @property
    def cite_as(self) -> str:
        return self.get_property("ietf:cite-as")

    @cite_as.setter
    def cite_as(self, value: str):
        self.set_property("ietf:cite-as", value)

    @property
    def item(self) -> Union["NotifyItem", None]:
        i = self.get_property("ietf:item")
        if i is not None:
            return NotifyItem(deepcopy(i),
                                 validate_stream_on_construct=False,
                                 validate_properties=self.validate_properties,
                                 validators=self.validators,
                                 validation_context="ietf:item")
        return None

    @item.setter
    def item(self, value: "NotifyItem"):
        self.set_property("ietf:item", value)

    @property
    def triple(self) -> tuple[str, str, str]:
        obj = self.get_property("as:object")
        rel = self.get_property("as:relationship")
        subj = self.get_property("as:subject")
        return obj, rel, subj

    @triple.setter
    def triple(self, value: tuple[str, str, str]):
        obj, rel, subj = value
        self.set_property("as:object", obj)
        self.set_property("as:relationship", rel)
        self.set_property("as:subject", subj)


class NotifyActor(NotifyDocumentPart):
    DEFAULT_TYPE = "Service"
    ALLOWED_TYPES = [DEFAULT_TYPE, "Application", "Group", "Organization", "Person"]

    @property
    def name(self) -> str:
        return self.get_property("name")

    @name.setter
    def name(self, value: str):
        self.set_property("name", value)


class NotifyItem(NotifyDocumentPart):

    @property
    def media_type(self) -> str:
        return self.get_property("mediaType")

    @media_type.setter
    def media_type(self, value: str):
        self.set_property("mediaType", value)
