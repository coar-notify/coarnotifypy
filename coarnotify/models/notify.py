from setuptools.config.pyprojecttoml import validate

from coarnotify.activitystreams2.activitystreams2 import ActivityStream, Properties, ActivityStreamsTypes, ACTIVITY_STREAMS_OBJECTS
from coarnotify import validate
from coarnotify.exceptions import ValidationError
from typing import Union
import uuid
from copy import deepcopy

NOTIFY_NAMESPACE = "https://coar-notify.net"


class NotifyProperties:
    INBOX = ("inbox", NOTIFY_NAMESPACE)
    CITE_AS = ("ietf:cite-as", NOTIFY_NAMESPACE)
    ITEM = ("ietf:item", NOTIFY_NAMESPACE)
    NAME = "name"
    MEDIA_TYPE = "mediaType"


class NotifyTypes:
    ENDORSMENT_ACTION = "coar-notify:EndorsementAction"
    INGEST_ACTION = "coar-notify:IngestAction"
    RELATIONSHIP_ACTION = "coar-notify:RelationshipAction"
    REVIEW_ACTION = "coar-notify:ReviewAction"
    UNPROCESSABLE_NOTIFICATION = "coar-notify:UnprocessableNotification"

    ABOUT_PAGE = "sorg:AboutPage"


VALIDATION_RULES = {
    Properties.ID: {
        "default": validate.absolute_uri,
        "context": {
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
        "default": validate.type_checker,
        "context": {
            Properties.ACTOR: {
                "default": validate.one_of([
                    ActivityStreamsTypes.SERVICE,
                    ActivityStreamsTypes.APPLICATION,
                    ActivityStreamsTypes.GROUP,
                    ActivityStreamsTypes.ORGANIZATION,
                    ActivityStreamsTypes.PERSON
                ])
            },

            Properties.OBJECT: {
                "default": validate.at_least_one_of(ACTIVITY_STREAMS_OBJECTS) #validate.contains("sorg:AboutPage"),
            },

            # Requirements say SHOULD, so will not validate at this stage
            # Properties.ORIGIN: {
            #     "default": validate.contains(ActivityStreamsTypes.SERVICE)
            # },

            # Requirements say SHOULD, so will not validate at this stage
            # Properties.TARGET: {
            #     "default": validate.contains(ActivityStreamsTypes.SERVICE)
            # },

            Properties.CONTEXT: {
                "default": validate.at_least_one_of(ACTIVITY_STREAMS_OBJECTS) #validate.contains("sorg:AboutPage"),
            },

            NotifyProperties.ITEM: {
                "default": validate.at_least_one_of(ACTIVITY_STREAMS_OBJECTS) #validate.contains("sorg:AboutPage"),
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

        self.required_and_validate(ve, Properties.ID, self.id)
        self.required_and_validate(ve, Properties.TYPE, self.type)

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
                    validator(self, value)
                except ValueError as ve:
                    if raise_error:
                        raise ve
                    else:
                        return False, str(ve)
        return True, ""

    def register_property_validation_error(self, ve: ValidationError, prop_name: Union[str, tuple], value):
        e, msg = self.validate_property(prop_name, value, force_validate=True, raise_error=False)
        if not e:
            ve.add_error(prop_name, msg)

    def required(self, ve: ValidationError, prop_name: Union[str, tuple], value):
        if value is None:
            pn = prop_name if not isinstance(prop_name, tuple) else prop_name[0]
            ve.add_error(prop_name, validate.REQUIRED_MESSAGE.format(x=pn))

    def required_and_validate(self, ve: ValidationError, prop_name: Union[str, tuple], value):
        if value is None:
            pn = prop_name if not isinstance(prop_name, tuple) else prop_name[0]
            ve.add_error(prop_name, validate.REQUIRED_MESSAGE.format(x=pn))
        else:
            if isinstance(value, NotifyBase):
                try:
                    value.validate()
                except ValidationError as subve:
                    ve.add_nested_errors(prop_name, subve)
            else:
                self.register_property_validation_error(ve, prop_name, value)

    def optional_and_validate(self, ve: ValidationError, prop_name: Union[str, tuple], value):
        if value is not None:
            if isinstance(value, NotifyBase):
                try:
                    value.validate()
                except ValidationError as subve:
                    ve.add_nested_errors(prop_name, subve)
            else:
                self.register_property_validation_error(ve, prop_name, value)

    def to_jsonld(self):
        return self._stream.to_jsonld()


class NotifyPattern(NotifyBase):
    TYPE = ActivityStreamsTypes.OBJECT

    def __init__(self, stream: Union[ActivityStream, dict] = None,
                 validate_stream_on_construct=True,
                 validate_properties=True,
                 validators=None,
                 validation_context=None):
        super(NotifyPattern, self).__init__(stream=stream,
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
            super(NotifyPattern, self).validate()
        except ValidationError as superve:
            ve = superve

        self.required_and_validate(ve, Properties.ORIGIN, self.origin)
        self.required_and_validate(ve, Properties.TARGET, self.target)
        self.required_and_validate(ve, Properties.OBJECT, self.object)
        self.optional_and_validate(ve, Properties.ACTOR, self.actor)
        self.optional_and_validate(ve, Properties.IN_REPLY_TO, self.in_reply_to)
        self.optional_and_validate(ve, Properties.CONTEXT, self.context)

        if ve.has_errors():
            raise ve

        return True


class NotifyPatternPart(NotifyBase):
    DEFAULT_TYPE = None
    ALLOWED_TYPES = []

    def __init__(self, stream: Union[ActivityStream, dict] = None,
                 validate_stream_on_construct=True,
                 validate_properties=True,
                 validators=None,
                 validation_context=None):
        super(NotifyPatternPart, self).__init__(stream=stream,
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

class NotifyService(NotifyPatternPart):
    DEFAULT_TYPE = ActivityStreamsTypes.SERVICE

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

        self.required_and_validate(ve, NotifyProperties.INBOX, self.inbox)

        if ve.has_errors():
            raise ve

        return True


class NotifyObject(NotifyPatternPart):
    """
    Can be used to represent an `object` or a `context`
    """

    @property
    def cite_as(self) -> str:
        return self.get_property(NotifyProperties.CITE_AS)

    @cite_as.setter
    def cite_as(self, value: str):
        self.set_property(NotifyProperties.CITE_AS, value)

    @property
    def item(self) -> Union["NotifyItem", None]:
        i = self.get_property(NotifyProperties.ITEM)
        if i is not None:
            return NotifyItem(deepcopy(i),
                                 validate_stream_on_construct=False,
                                 validate_properties=self.validate_properties,
                                 validators=self.validators,
                                 validation_context=NotifyProperties.ITEM)
        return None

    @item.setter
    def item(self, value: "NotifyItem"):
        self.set_property(NotifyProperties.ITEM, value)

    @property
    def triple(self) -> tuple[str, str, str]:
        obj = self.get_property(Properties.OBJECT_TRIPLE)
        rel = self.get_property(Properties.RELATIONSHIP_TRIPLE)
        subj = self.get_property(Properties.SUBJECT_TRIPLE)
        return obj, rel, subj

    @triple.setter
    def triple(self, value: tuple[str, str, str]):
        obj, rel, subj = value
        self.set_property(Properties.OBJECT_TRIPLE, obj)
        self.set_property(Properties.RELATIONSHIP_TRIPLE, rel)
        self.set_property(Properties.SUBJECT_TRIPLE, subj)

    def validate(self):
        # Object does not require `type`, so we override the base validator to just validate
        # the id
        ve = ValidationError()

        self.required_and_validate(ve, Properties.ID, self.id)

        if ve.has_errors():
            raise ve
        return True


class NotifyActor(NotifyPatternPart):
    DEFAULT_TYPE = ActivityStreamsTypes.SERVICE
    ALLOWED_TYPES = [DEFAULT_TYPE,
                     ActivityStreamsTypes.APPLICATION,
                     ActivityStreamsTypes.GROUP,
                     ActivityStreamsTypes.ORGANIZATION,
                     ActivityStreamsTypes.PERSON
                     ]

    @property
    def name(self) -> str:
        return self.get_property(NotifyProperties.NAME)

    @name.setter
    def name(self, value: str):
        self.set_property(NotifyProperties.NAME, value)


class NotifyItem(NotifyPatternPart):

    @property
    def media_type(self) -> str:
        return self.get_property(NotifyProperties.MEDIA_TYPE)

    @media_type.setter
    def media_type(self, value: str):
        self.set_property(NotifyProperties.MEDIA_TYPE, value)

    def validate(self):
        # Item does not always require a type, so override the base validator
        ve = ValidationError()

        self.required_and_validate(ve, Properties.ID, self.id)

        if ve.has_errors():
            raise ve
        return True


## Mixins
##########################################################

class NestedPatternObjectMixin(object):
    @property
    def object(self) -> Union[NotifyPattern, NotifyObject, None]:
        o = self.get_property(Properties.OBJECT)
        if o is not None:
            from coarnotify.factory import COARNotifyFactory  # late import to avoid circular dependency
            nested = COARNotifyFactory.get_by_object(deepcopy(o),
                                                     validate_stream_on_construct=False,
                                                     validate_properties=self.validate_properties,
                                                     validators=self.validators,
                                                     validation_context=None)  # don't supply a validation context, as these objects are not typical nested objects
            if nested is not None:
                return nested

            # if we are unable to construct the typed nested object, just return a generic object
            return NotifyObject(deepcopy(o),
                                validate_stream_on_construct=False,
                                validate_properties=self.validate_properties,
                                validators=self.validators,
                                validation_context=Properties.OBJECT)
        return None

    @object.setter
    def object(self, value: Union[NotifyObject, NotifyPattern]):
        self.set_property(Properties.OBJECT, value.doc)


class SummaryMixin(object):
    @property
    def summary(self) -> str:
        return self.get_property(Properties.SUMMARY)

    @summary.setter
    def summary(self, summary: str):
        self.set_property(Properties.SUMMARY, summary)