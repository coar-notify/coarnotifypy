"""
This module is home to all the core model objects from which the notify patterns extend
"""

from coarnotify.core.activitystreams2 import ActivityStream, Properties, ActivityStreamsTypes, ACTIVITY_STREAMS_OBJECTS
from coarnotify import validate
from coarnotify.exceptions import ValidationError
from typing import Union, Tuple
import uuid
from copy import deepcopy

NOTIFY_NAMESPACE = "https://coar-notify.net"
"""Namespace for COAR Notify, to be used to construct namespaced properties used in COAR Notify Patterns"""

class NotifyProperties:
    """
    COAR Notify properties used in COAR Notify Patterns

    Most of these are provided as tuples, where the first element is the property name, and the second element is the namespace.
    Some are provided as plain strings without namespaces

    These are suitable to be used as property names in all the property getters/setters in the notify pattern objects
    and in the validation configuration.
    """
    INBOX = ("inbox", NOTIFY_NAMESPACE)
    """``inbox`` property"""

    CITE_AS = ("ietf:cite-as", NOTIFY_NAMESPACE)
    """``ietf:cite-as`` property"""

    ITEM = ("ietf:item", NOTIFY_NAMESPACE)
    """``ietf:item`` property"""

    NAME = "name"
    """``name`` property"""

    MEDIA_TYPE = "mediaType"
    """``mediaType`` property"""

class NotifyTypes:
    """
    List of all the COAR Notify types patterns may use.

    These are in addition to the base Activity Streams types, which are in :py:class:`coarnotify.core.activitystreams2.ActivityStreamsTypes`
    """
    ENDORSMENT_ACTION = "coar-notify:EndorsementAction"
    INGEST_ACTION = "coar-notify:IngestAction"
    RELATIONSHIP_ACTION = "coar-notify:RelationshipAction"
    REVIEW_ACTION = "coar-notify:ReviewAction"
    UNPROCESSABLE_NOTIFICATION = "coar-notify:UnprocessableNotification"

    ABOUT_PAGE = "sorg:AboutPage"


_VALIDATION_RULES = {
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

VALIDATORS: validate.Validator = validate.Validator(_VALIDATION_RULES)
"""Default Validator object for all pattern types, of type :py:class:`coarnotify.validate.Validator`"""


class NotifyBase:
    """
    Base class from which all Notify objects extend.

    There are two kinds of Notify objects:

    1. Patterns, which are the notifications themselves
    2. Pattern Parts, which are nested elements in the Patterns, such as objects, contexts, actors, etc

    This class forms the basis for both of those types, and provides essential services,
    such as construction, accessors and validation, as well as supporting the essential
    properties "id" and "type"
    """
    def __init__(self, stream: Union[ActivityStream, dict] = None,
                 validate_stream_on_construct: bool=True,
                 validate_properties: bool=True,
                 validators: validate.Validator=None,
                 validation_context: Union[str, Tuple[str, str]]=None,
                 properties_by_reference: bool=True):
        """
        Base constructor that all subclasses should call

        :param stream:  The activity stream object, or a dict from which one can be created
        :param validate_stream_on_construct:    should the incoming stream be validated at construction-time
        :param validate_properties:     should individual properties be validated as they are set
        :param validators:      the validator object for this class and all nested elements.  If not provided will use the default :py:data:`VALIDATORS`
        :param validation_context:  the context in which this object is being validated.  This is used to determine which validators to use
        :param properties_by_reference:     should properties be get and set by reference (the default) or by value.  Use this with caution: setting by value
            makes it impossible to set a property in a nested object using the dot notation, like ``obj.actor.name = "Bob"``, instead you will need to retrive
            the object, set the value, then set the whole object back on the parent object.
        """
        self._validate_stream_on_construct = validate_stream_on_construct
        self._validate_properties = validate_properties
        self._validators = validators if validators is not None else VALIDATORS
        self._validation_context = validation_context
        self._properties_by_reference = properties_by_reference
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
    def validate_properties(self) -> bool:
        """Are properties being validated on set"""
        return self._validate_properties

    @property
    def validate_stream_on_construct(self) -> bool:
        """Is the stream validated on construction"""
        return self._validate_stream_on_construct

    @property
    def validators(self) -> validate.Validator:
        """The validator object for this instance"""
        return self._validators

    @property
    def doc(self):
        """The underlying ActivityStream object, excluding the JSON-LD @context"""
        return self._stream.doc

    @property
    def id(self) -> str:
        """The ``id`` of the object"""
        return self.get_property(Properties.ID)

    @id.setter
    def id(self, value: str):
        self.set_property(Properties.ID, value)

    @property
    def type(self) -> Union[str, list[str]]:
        """The ``type`` of the object"""
        return self.get_property(Properties.TYPE)

    @type.setter
    def type(self, types: Union[str, list[str]]):
        self.set_property(Properties.TYPE, types)

    def get_property(self, prop_name: Union[str, Tuple[str, str]], by_reference: bool=None):
        """
        Generic property getter.  It is strongly recommended that all accessors proxy for this function
        as this enforces by-reference/by-value accessing, and mediates directly with the underlying
        activity stream object.

        :param prop_name: The property to retrieve
        :param by_reference: Whether to retrieve by_reference or by_value.  If not supplied will default to the object-wide setting
        :return: the property value
        """
        if by_reference is None:
            by_reference = self._properties_by_reference
        val = self._stream.get_property(prop_name)
        if by_reference:
            return val
        else:
            return deepcopy(val)

    def set_property(self, prop_name: Union[str, Tuple[str, str]], value, by_reference: bool=None):
        """
        Generic property setter.  It is strongly recommended that all accessors proxy for this function
        as this enforces by-reference/by-value accessing, and mediates directly with the underlying
        activity stream object.

        :param prop_name: The property to set
        :param value: The value to set
        :param by_reference: Whether to set by_reference or by_value.  If not supplied will default to the object-wide setting
        """
        if by_reference is None:
            by_reference = self._properties_by_reference
        self.validate_property(prop_name, value)
        if not by_reference:
            value = deepcopy(value)
        self._stream.set_property(prop_name, value)

    def validate(self) -> bool:
        """
        Validate the object.  This provides the basic validation on ``id`` and ``type``.
        Subclasses should override this method with their own validation, and call this method via ``super`` first to ensure
        the basic properties are validated.

        :return: ``True`` or raise a :py:class:`coarnotify.exceptions.ValidationError` if there are errors
        """
        ve = ValidationError()

        self.required_and_validate(ve, Properties.ID, self.id)
        self.required_and_validate(ve, Properties.TYPE, self.type)

        if ve.has_errors():
            raise ve
        return True

    def validate_property(self, prop_name: Union[str, Tuple[str, str]], value,
                          force_validate: bool=False, raise_error: bool=True) -> Tuple[bool, str]:
        """
        Validate a single property.  This is used internally by :py:meth:`set_property`.

        If the object has ``validate_properties`` set to ``False`` then that behaviour may be overridden by setting ``force_validate`` to ``True``

        The validator applied to the property will be determined according to the ``validators`` property of the object
        and the ``validation_context`` of the object.

        :param prop_name: The property to validate
        :param value:  the value to validate
        :param force_validate:  whether to validate anyway, even if property validation is turned off at the object level
        :param raise_error: raise an exception on validation failure, or return a tuple with the result
        :return: A tuple of whether validation was successful, and the error message if it was not
            (the empty string is returned as the second element if validation was successful)
        """
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

    def _register_property_validation_error(self, ve: ValidationError, prop_name: Union[str, tuple], value):
        """Force validate the property and if an error is found, add it to the validation error"""
        e, msg = self.validate_property(prop_name, value, force_validate=True, raise_error=False)
        if not e:
            ve.add_error(prop_name, msg)

    def required(self, ve: ValidationError, prop_name: Union[str, tuple], value):
        """
        Add a required error to the validation error if the value is None

        :param ve: The validation error to which to add the message
        :param prop_name:   The property to check
        :param value:   The value
        """
        if value is None:
            pn = prop_name if not isinstance(prop_name, tuple) else prop_name[0]
            ve.add_error(prop_name, validate.REQUIRED_MESSAGE.format(x=pn))

    def required_and_validate(self, ve: ValidationError, prop_name: Union[str, tuple], value):
        """
        Add a required error to the validation error if the value is None, and then validate the value if not.

        Any error messages are added to the ``ValidationError`` object

        :param ve: the validation error to which to add the message
        :param prop_name: The property to check
        :param value: the value to check
        """
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
                self._register_property_validation_error(ve, prop_name, value)

    def optional_and_validate(self, ve: ValidationError, prop_name: Union[str, tuple], value):
        """
        Validate the value if it is not None, but do not raise a validation error if it is None

        :param ve:
        :param prop_name:
        :param value:
        :return:
        """
        if value is not None:
            if isinstance(value, NotifyBase):
                try:
                    value.validate()
                except ValidationError as subve:
                    ve.add_nested_errors(prop_name, subve)
            else:
                self._register_property_validation_error(ve, prop_name, value)

    def to_jsonld(self) -> dict:
        """
        Get the notification pattern as JSON-LD

        :return: JSON-LD representation of the pattern
        """
        return self._stream.to_jsonld()


class NotifyPattern(NotifyBase):
    """
    Base class for all notification patterns
    """
    TYPE = ActivityStreamsTypes.OBJECT
    """The type of the pattern.  This should be overridden by subclasses, otherwise defaults to ``Object``"""

    def __init__(self, stream: Union[ActivityStream, dict] = None,
                 validate_stream_on_construct=True,
                 validate_properties=True,
                 validators=None,
                 validation_context=None,
                 properties_by_reference=True):
        """
        Constructor for the NotifyPattern

        This constructor will ensure that the pattern has its mandated type :py:attr:`TYPE` in the ``type`` property

        :param stream:  The activity stream object, or a dict from which one can be created
        :param validate_stream_on_construct:    should the incoming stream be validated at construction-time
        :param validate_properties:     should individual properties be validated as they are set
        :param validators:      the validator object for this class and all nested elements.  If not provided will use the default :py:data:`VALIDATORS`
        :param validation_context:  the context in which this object is being validated.  This is used to determine which validators to use
        :param properties_by_reference:     should properties be get and set by reference (the default) or by value.  Use this with caution: setting by value
            makes it impossible to set a property in a nested object using the dot notation, like ``obj.actor.name = "Bob"``, instead you will need to retrive
            the object, set the value, then set the whole object back on the parent object.
        """
        super(NotifyPattern, self).__init__(stream=stream,
                                            validate_stream_on_construct=validate_stream_on_construct,
                                            validate_properties=validate_properties,
                                            validators=validators,
                                            validation_context=validation_context,
                                            properties_by_reference=properties_by_reference)
        self._ensure_type_contains(self.TYPE)

    def _ensure_type_contains(self, types: Union[str, list[str]]):
        """Ensure that the type field contains the given types"""
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
        """Get the origin property of the notification"""
        o = self.get_property(Properties.ORIGIN)
        if o is not None:
            return NotifyService(o,
                                 validate_stream_on_construct=False,
                                 validate_properties=self.validate_properties,
                                 validators=self.validators,
                                 validation_context=Properties.ORIGIN,
                                 properties_by_reference=self._properties_by_reference)
        return None

    @origin.setter
    def origin(self, value: "NotifyService"):
        self.set_property(Properties.ORIGIN, value.doc)

    @property
    def target(self) -> Union["NotifyService", None]:
        """Get the target property of the notification"""
        t = self.get_property(Properties.TARGET)
        if t is not None:
            return NotifyService(t,
                                 validate_stream_on_construct=False,
                                 validate_properties=self.validate_properties,
                                 validators=self.validators,
                                 validation_context=Properties.TARGET,
                                 properties_by_reference=self._properties_by_reference)
        return None

    @target.setter
    def target(self, value: "NotifyService"):
        self.set_property(Properties.TARGET, value.doc)

    @property
    def object(self) -> Union["NotifyObject", None]:
        """Get the object property of the notification"""
        o = self.get_property(Properties.OBJECT)
        if o is not None:
            return NotifyObject(o,
                            validate_stream_on_construct=False,
                            validate_properties=self.validate_properties,
                            validators=self.validators,
                            validation_context=Properties.OBJECT,
                            properties_by_reference=self._properties_by_reference)
        return None

    @object.setter
    def object(self, value: "NotifyObject"):
        self.set_property(Properties.OBJECT, value.doc)

    @property
    def in_reply_to(self) -> str:
        """Get the inReplyTo property of the notification"""
        return self.get_property(Properties.IN_REPLY_TO)

    @in_reply_to.setter
    def in_reply_to(self, value: str):
        self.set_property(Properties.IN_REPLY_TO, value)

    @property
    def actor(self) -> Union["NotifyActor", None]:
        """Get the actor property of the notification"""
        a = self.get_property(Properties.ACTOR)
        if a is not None:
            return NotifyActor(a,
                            validate_stream_on_construct=False,
                            validate_properties=self.validate_properties,
                            validators=self.validators,
                            validation_context=Properties.ACTOR,
                            properties_by_reference=self._properties_by_reference)
        return None

    @actor.setter
    def actor(self, value: "NotifyActor"):
        self.set_property(Properties.ACTOR, value.doc)

    @property
    def context(self) -> Union["NotifyObject", None]:
        """Get the context property of the notification"""
        c = self.get_property(Properties.CONTEXT)
        if c is not None:
            return NotifyObject(c,
                            validate_stream_on_construct=False,
                            validate_properties=self.validate_properties,
                            validators=self.validators,
                            validation_context=Properties.CONTEXT,
                            properties_by_reference=self._properties_by_reference)
        return None

    @context.setter
    def context(self, value: "NotifyObject"):
        self.set_property(Properties.CONTEXT, value.doc)

    def validate(self) -> bool:
        """
        Base validator for all notification patterns.  This extends the validate function on the superclass.

        In addition to the base class's constraints, this applies the following validation:

        * The ``origin``, ``target`` and ``object`` properties are required and must be valid
        * The ``actor`` ``inReplyTo`` and ``context`` properties are optional, but if present must be valid

        :py:class:`NotifyBase`
        :return: ``True`` if valid, otherwise raises :py:class:`coarnotify.exceptions.ValidationError`
        """
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
    """
    Base class for all pattern parts, such as objects, contexts, actors, etc

    If there is a default type specified, and a type is not given at construction, then
    the default type will be added

    :param stream:  The activity stream object, or a dict from which one can be created
    :param validate_stream_on_construct:    should the incoming stream be validated at construction-time
    :param validate_properties:     should individual properties be validated as they are set
    :param validators:      the validator object for this class and all nested elements.  If not provided will use the default :py:data:`VALIDATORS`
    :param validation_context:  the context in which this object is being validated.  This is used to determine which validators to use
    :param properties_by_reference:     should properties be get and set by reference (the default) or by value.  Use this with caution: setting by value
        makes it impossible to set a property in a nested object using the dot notation, like ``obj.actor.name = "Bob"``, instead you will need to retrive
        the object, set the value, then set the whole object back on the parent object.
    """
    DEFAULT_TYPE = None
    """The default type for this object, if none is provided on construction.  If not provided, then no default type will be set"""

    ALLOWED_TYPES = []
    """The list of types that are permissable for this object.  If the list is empty, then any type is allowed"""

    def __init__(self, stream: Union[ActivityStream, dict] = None,
                 validate_stream_on_construct=True,
                 validate_properties=True,
                 validators=None,
                 validation_context=None,
                 properties_by_reference=True):
        """
        Constructor for the NotifyPatternPart

        If there is a default type specified, and a type is not given at construction, then
        the default type will be added

        :param stream:  The activity stream object, or a dict from which one can be created
        :param validate_stream_on_construct:    should the incoming stream be validated at construction-time
        :param validate_properties:     should individual properties be validated as they are set
        :param validators:      the validator object for this class and all nested elements.  If not provided will use the default :py:data:`VALIDATORS`
        :param validation_context:  the context in which this object is being validated.  This is used to determine which validators to use
        :param properties_by_reference:     should properties be get and set by reference (the default) or by value.  Use this with caution: setting by value
            makes it impossible to set a property in a nested object using the dot notation, like ``obj.actor.name = "Bob"``, instead you will need to retrive
            the object, set the value, then set the whole object back on the parent object.
        """
        super(NotifyPatternPart, self).__init__(stream=stream,
                                                validate_stream_on_construct=validate_stream_on_construct,
                                                validate_properties=validate_properties,
                                                validators=validators,
                                                validation_context=validation_context,
                                                properties_by_reference=properties_by_reference)
        if self.DEFAULT_TYPE is not None and self.type is None:
            self.type = self.DEFAULT_TYPE

    @NotifyBase.type.setter
    def type(self, types: Union[str, list[str]]):
        """Set the type of the object, and validate that it is one of the allowed types if present"""
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
    """
    Default class to represent a service in the COAR Notify pattern.

    Services are used to represent ``origin`` and ``target`` properties in the notification patterns

    Specific patterns may need to extend this class to provide their specific behaviours and validation
    """
    DEFAULT_TYPE = ActivityStreamsTypes.SERVICE
    """The default type for a service is ``Service``, but the type can be set to any value"""

    @property
    def inbox(self) -> str:
        """Get the ``inbox`` property of the service"""
        return self.get_property(NotifyProperties.INBOX)

    @inbox.setter
    def inbox(self, value: str):
        self.set_property(NotifyProperties.INBOX, value)


class NotifyObject(NotifyPatternPart):
    """
    Deafult class to represent an object in the COAR Notify pattern.  Objects can be used for ``object`` or ``context`` properties
    in notify patterns

    Specific patterns may need to extend this class to provide their specific behaviours and validation
    """

    @property
    def cite_as(self) -> str:
        """Get the ``ietf:cite-as`` property of the object"""
        return self.get_property(NotifyProperties.CITE_AS)

    @cite_as.setter
    def cite_as(self, value: str):
        self.set_property(NotifyProperties.CITE_AS, value)

    @property
    def item(self) -> Union["NotifyItem", None]:
        """Get the ``ietf:item`` property of the object"""
        i = self.get_property(NotifyProperties.ITEM)
        if i is not None:
            return NotifyItem(i,
                            validate_stream_on_construct=False,
                            validate_properties=self.validate_properties,
                            validators=self.validators,
                            validation_context=NotifyProperties.ITEM,
                            properties_by_reference=self._properties_by_reference)
        return None

    @item.setter
    def item(self, value: "NotifyItem"):
        self.set_property(NotifyProperties.ITEM, value)

    @property
    def triple(self) -> tuple[str, str, str]:
        """Get object, relationship and subject properties as a relationship triple"""
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

    def validate(self) -> bool:
        """
        Validate the object.  This overrides the base validation, as objects only absolutely require an ``id`` property,
        so the base requirement for a ``type`` is relaxed.

        :return: ``True`` if valid, otherwise raises :py:class:`coarnotify.exceptions.ValidationError`
        """
        ve = ValidationError()

        self.required_and_validate(ve, Properties.ID, self.id)

        if ve.has_errors():
            raise ve
        return True


class NotifyActor(NotifyPatternPart):
    """
    Deafult class to represents an actor in the COAR Notify pattern.
    Actors are used to represent the ``actor`` property in the notification patterns

    Specific patterns may need to extend this class to provide their specific behaviours and validation
    """
    DEFAULT_TYPE = ActivityStreamsTypes.SERVICE
    """Default type is ``Service``, but can also be set as any one of the other allowed types"""

    ALLOWED_TYPES = [DEFAULT_TYPE,
                     ActivityStreamsTypes.APPLICATION,
                     ActivityStreamsTypes.GROUP,
                     ActivityStreamsTypes.ORGANIZATION,
                     ActivityStreamsTypes.PERSON
                     ]
    """The allowed types for an actor: ``Service``, ``Application``, ``Group``, ``Organisation``, ``Person``"""

    @property
    def name(self) -> str:
        """Get the name property of the actor"""
        return self.get_property(NotifyProperties.NAME)

    @name.setter
    def name(self, value: str):
        self.set_property(NotifyProperties.NAME, value)


class NotifyItem(NotifyPatternPart):
    """
    Defult class to represent an item in the COAR Notify pattern.
    Items are used to represent the ``ietf:item`` property in the notification patterns

    Specific patterns may need to extend this class to provide their specific behaviours and validation
    """
    @property
    def media_type(self) -> str:
        """Get the ``mediaType`` property of the item"""
        return self.get_property(NotifyProperties.MEDIA_TYPE)

    @media_type.setter
    def media_type(self, value: str):
        self.set_property(NotifyProperties.MEDIA_TYPE, value)

    def validate(self):
        """
        Validate the item.  This overrides the base validation, as objects only absolutely require an ``id`` property,
        so the base requirement for a ``type`` is relaxed.

        :return: ``True`` if valid, otherwise raises :py:class:`coarnotify.exceptions.ValidationError`
        """
        ve = ValidationError()

        self.required_and_validate(ve, Properties.ID, self.id)

        if ve.has_errors():
            raise ve
        return True


## Mixins
##########################################################

class NestedPatternObjectMixin:
    """
    A mixin to add to a pattern which can override the default object property to return a full
    nested pattern from the ``object`` property, rather than the default :py:class:`NotifyObject`

    This mixin needs to be first on the inheritance list, as it overrides the object property
    of the NotifyPattern class.

    For example:

    .. code-block:: python

        class MySpecialPattern(NestedPatternObjectMixin, NotifyPattern):
            pass
    """
    @property
    def object(self) -> Union[NotifyPattern, NotifyObject, None]:
        """Retrieve an object as it's correctly typed pattern, falling back to a default ``NotifyObject`` if no pattern matches"""
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


class SummaryMixin:
    """
    Mixin to provide an API for setting and getting the ``summary`` property of a pattern
    """
    @property
    def summary(self) -> str:
        """The summary property of the pattern"""
        return self.get_property(Properties.SUMMARY)

    @summary.setter
    def summary(self, summary: str):
        self.set_property(Properties.SUMMARY, summary)