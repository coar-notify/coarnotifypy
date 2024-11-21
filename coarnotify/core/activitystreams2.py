"""
This module contains everything COAR Notify needs to know about ActivityStreams 2.0
https://www.w3.org/TR/activitystreams-core/

It provides knowledge of the essential AS properties and types, and a class to wrap
ActivityStreams objects and provide a simple interface to work with them.

**NOTE** this is not a complete implementation of AS 2.0, it is **only** what is required
to work with COAR Notify patterns.
"""
from typing import Union


ACTIVITY_STREAMS_NAMESPACE = "https://www.w3.org/ns/activitystreams"
"""Namespace for Actvitity Streams, to be used to construct namespaced properties used in COAR Notify Patterns"""

class Properties:
    """
    ActivityStreams 2.0 properties used in COAR Notify Patterns

    These are provided as tuples, where the first element is the property name, and the second element is the namespace.

    These are suitbale to be used as property names in all the property getters/setters in the notify pattern objects
    and in the validation configuration.
    """
    ID = ("id", ACTIVITY_STREAMS_NAMESPACE)
    """``id`` property"""

    TYPE = ("type", ACTIVITY_STREAMS_NAMESPACE)
    """``type`` property"""

    ORIGIN = ("origin", ACTIVITY_STREAMS_NAMESPACE)
    """``origin`` property"""

    OBJECT = ("object", ACTIVITY_STREAMS_NAMESPACE)
    """``object`` property"""

    TARGET = ("target", ACTIVITY_STREAMS_NAMESPACE)
    """``target`` property"""

    ACTOR = ("actor", ACTIVITY_STREAMS_NAMESPACE)
    """``actor`` property"""

    IN_REPLY_TO = ("inReplyTo", ACTIVITY_STREAMS_NAMESPACE)
    """``inReplyTo`` property"""

    CONTEXT = ("context", ACTIVITY_STREAMS_NAMESPACE)
    """``context`` property"""

    SUMMARY = ("summary", ACTIVITY_STREAMS_NAMESPACE)
    """``summary`` property"""

    SUBJECT_TRIPLE = ("as:subject", ACTIVITY_STREAMS_NAMESPACE)
    """``as:subject`` property"""

    OBJECT_TRIPLE = ("as:object", ACTIVITY_STREAMS_NAMESPACE)
    """``as:object`` property"""

    RELATIONSHIP_TRIPLE = ("as:relationship", ACTIVITY_STREAMS_NAMESPACE)
    """``as:relationship`` property"""

class ActivityStreamsTypes:
    """
    List of all the Activity Streams types COAR Notify may use.

    Note that COAR Notify also has its own custom types and they are defined in
    :py:class:`coarnotify.models.notify.NotifyTypes`
    """

    # Activities
    ACCEPT = "Accept"
    ANNOUNCE = "Announce"
    REJECT = "Reject"
    OFFER = "Offer"
    TENTATIVE_ACCEPT = "TentativeAccept"
    TENTATIVE_REJECT = "TentativeReject"
    FLAG = "Flag"
    UNDO = "Undo"

    # Objects
    ACTIVITY = "Activity"
    APPLICATION = "Application"
    ARTICLE = "Article"
    AUDIO = "Audio"
    COLLECTION = "Collection"
    COLLECTION_PAGE = "CollectionPage"
    RELATIONSHIP = "Relationship"
    DOCUMENT = "Document"
    EVENT = "Event"
    GROUP = "Group"
    IMAGE = "Image"
    INTRANSITIVE_ACTIVITY = "IntransitiveActivity"
    NOTE = "Note"
    OBJECT = "Object"
    ORDERED_COLLECTION = "OrderedCollection"
    ORDERED_COLLECTION_PAGE = "OrderedCollectionPage"
    ORGANIZATION = "Organization"
    PAGE = "Page"
    PERSON = "Person"
    PLACE = "Place"
    PROFILE = "Profile"
    QUESTION = "Question"
    SERVICE = "Service"
    TOMBSTONE = "Tombstone"
    VIDEO = "Video"

ACTIVITY_STREAMS_OBJECTS = [
    ActivityStreamsTypes.ACTIVITY,
    ActivityStreamsTypes.APPLICATION,
    ActivityStreamsTypes.ARTICLE,
    ActivityStreamsTypes.AUDIO,
    ActivityStreamsTypes.COLLECTION,
    ActivityStreamsTypes.COLLECTION_PAGE,
    ActivityStreamsTypes.RELATIONSHIP,
    ActivityStreamsTypes.DOCUMENT,
    ActivityStreamsTypes.EVENT,
    ActivityStreamsTypes.GROUP,
    ActivityStreamsTypes.IMAGE,
    ActivityStreamsTypes.INTRANSITIVE_ACTIVITY,
    ActivityStreamsTypes.NOTE,
    ActivityStreamsTypes.OBJECT,
    ActivityStreamsTypes.ORDERED_COLLECTION,
    ActivityStreamsTypes.ORDERED_COLLECTION_PAGE,
    ActivityStreamsTypes.ORGANIZATION,
    ActivityStreamsTypes.PAGE,
    ActivityStreamsTypes.PERSON,
    ActivityStreamsTypes.PLACE,
    ActivityStreamsTypes.PROFILE,
    ActivityStreamsTypes.QUESTION,
    ActivityStreamsTypes.SERVICE,
    ActivityStreamsTypes.TOMBSTONE,
    ActivityStreamsTypes.VIDEO
]
"""The sub-list of ActivityStreams types that are also objects in AS 2.0"""

class ActivityStream:
    """
    A simple wrapper around an ActivityStreams dictionary object

    Construct it with a python dictionary that represents an ActivityStreams object, or
    without to create a fresh, blank object.

    :param raw: the raw ActivityStreams object, as a dictionary
    """
    def __init__(self, raw: dict=None):
        """
        Construct a new ActivityStream object

        :param raw: the raw ActivityStreams object, as a dictionary
        """
        self._doc = raw if raw is not None else {}
        self._context = []
        if "@context" in self._doc:
            self._context = self._doc["@context"]
            if not isinstance(self._context, list):
                self._context = [self._context]
            del self._doc["@context"]

    @property
    def doc(self) -> dict:
        """The internal dictionary representation of the ActivityStream, without the json-ld context"""
        return self._doc

    @doc.setter
    def doc(self, doc:dict):
        self._doc = doc

    @property
    def context(self):
        """The json-ld context of the ActivityStream"""
        return self._context

    @context.setter
    def context(self, context):
        self._context = context

    def _register_namespace(self, namespace: Union[str, tuple[str, str]]):
        """
        Register a namespace in the context of the ActivityStream
        """
        entry = namespace
        if isinstance(namespace, tuple):
            url = namespace[1]
            short = namespace[0]
            entry = {short: url}

        if entry not in self._context:
            self._context.append(entry)

    def set_property(self, property: Union[str, tuple[str, str], tuple[str, tuple[str, str]]], value):
        """
        Set an arbitrary property on the object.  The property name can be one of:

        * A simple string with the property name
        * A tuple of the property name and the full namespace ``("name", "http://example.com/ns")``
        * A tuple containing the property name and another tuple of the short name and the full namespace ``("name", ("as", "http://example.com/ns"))``

        :param property: the property name
        :param value: the value to set
        """
        prop_name = property
        namespace = None
        if isinstance(property, tuple):
            prop_name = property[0]
            namespace = property[1]

        self._doc[prop_name] = value
        if namespace is not None:
            self._register_namespace(namespace)

    def get_property(self, property: Union[str, tuple[str, str], tuple[str, tuple[str, str]]]):
        """
        Get an arbitrary property on the object.  The property name can be one of:

        * A simple string with the property name
        * A tuple of the property name and the full namespace ``("name", "http://example.com/ns")``
        * A tuple containing the property name and another tuple of the short name and the full namespace ``("name", ("as", "http://example.com/ns"))``

        :param property:   the property name
        :return: the value of the property, or None if it does not exist
        """
        prop_name = property
        namespace = None
        if isinstance(property, tuple):
            prop_name = property[0]
            namespace = property[1]

        return self._doc.get(prop_name, None)

    def to_jsonld(self) -> dict:
        """
        Get the activity stream as a JSON-LD object

        :return:
        """
        return {
            "@context": self._context,
            **self._doc
        }