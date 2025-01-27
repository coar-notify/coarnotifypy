"""
Factory for producing the correct model based on the type or data within a payload
"""

from typing import List, Callable, Union
from coarnotify.core.activitystreams2 import ActivityStream, Properties
from coarnotify.core.notify import NotifyPattern
from coarnotify.patterns import (
    Accept,
    AnnounceEndorsement,
    AnnounceRelationship,
    AnnounceReview,
    AnnounceServiceResult,
    Reject,
    RequestEndorsement,
    RequestReview,
    TentativelyAccept,
    TentativelyReject,
    UnprocessableNotification,
    UndoOffer
)
from coarnotify.exceptions import NotifyException


class COARNotifyFactory:
    """
    Factory for producing the correct model based on the type or data within a payload
    """

    MODELS = [
        Accept,
        AnnounceEndorsement,
        AnnounceRelationship,
        AnnounceReview,
        AnnounceServiceResult,
        Reject,
        RequestEndorsement,
        RequestReview,
        TentativelyAccept,
        TentativelyReject,
        UnprocessableNotification,
        UndoOffer
    ]
    """The list of model classes recognised by this factory"""

    @classmethod
    def get_by_types(cls, incoming_types:Union[str, List[str]]) -> Union[Callable, None]:
        """
        Get the model class based on the supplied types.  The returned callable is the class, not an instance.

        This is achieved by inspecting all of the known types in ``MODELS``, and performing the following
        calculation:

        1. If the supplied types are a subset of the model types, then this is a candidate, keep a reference to it
        2. If the candidate fit is exact (supplied types and model types are the same), return the class
        3. If the class is a better fit than the last candidate, update the candidate.  If the fit is exact, return the class
        4. Once we have run out of models to check, return the best candidate (or None if none found)

        :param incoming_types: a single type or list of types.  If a list is provided, ALL types must match a candidate
        :return:    A class representing the best fit for the supplied types, or ``None`` if no match
        """
        if not isinstance(incoming_types, list):
            incoming_types = [incoming_types]

        candidate = None
        candidate_fit = None

        for m in cls.MODELS:
            document_types = m.TYPE
            if not isinstance(document_types, list):
                document_types = [document_types]
            if set(document_types).issubset(set(incoming_types)):
                if candidate_fit is None:
                    candidate = m
                    candidate_fit = len(incoming_types) - len(document_types)
                    if candidate_fit == 0:
                        return candidate

                else:
                    fit = len(incoming_types) - len(document_types)
                    if fit == 0:
                        return m
                    if abs(fit) < abs(candidate_fit):
                        candidate = m
                        candidate_fit = fit

        return candidate

    @classmethod
    def get_by_object(cls, data: dict, *args, **kwargs) -> NotifyPattern:
        """
        Get an instance of a model based on the data provided.

        Internally this calls ``get_by_types`` to determine the class to instantiate, and then creates an instance of that
        Using the supplied args and kwargs.

        If a model cannot be found that matches the data, a NotifyException is raised.

        :param data: The raw stream data to parse and instantiate around
        :param args: any args to pass to the object constructor
        :param kwargs: any kwargs to pass to the object constructor
        :return: A NotifyPattern of the correct type, wrapping the data
        """
        stream = ActivityStream(data)

        types = stream.get_property(Properties.TYPE)
        if types is None:
            raise NotifyException("No type found in object")

        klazz = cls.get_by_types(types)

        inst = klazz(data, *args, **kwargs)
        return inst

    @classmethod
    def register(cls, model: NotifyPattern):
        existing = cls.get_by_types(model.TYPE)
        if existing is not None:
            cls.MODELS.remove(existing)
        cls.MODELS.append(model)