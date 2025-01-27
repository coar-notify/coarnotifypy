"""
This module provides a set of validation functions that can be used to validate properties on objects.
It also contains a ``Validator`` class which is used to wrap the protocol-wide validation rules which
are shared across all objects.
"""

from urllib.parse import urlparse
import re
from typing import Union, Tuple, Callable, List

# mostly to help us with generating the correct documentation
__all__ = ('Validator', 'absolute_uri', 'url', 'one_of', 'at_least_one_of', 'contains', 'type_checker')

REQUIRED_MESSAGE = "`{x}` is a required field"

class Validator:
    """
    A wrapper around a set of validation rules which can be used to select the appropriate validator
    in a given context.

    The validation rules are structured as follows:

    .. code-block:: python

        {
            "<property>": {
                "default": default_validator_function
                "context": {
                    "<context>": {
                        "default": default_validator_function
                    }
                }
            }
        }

    Here the ``<property>`` key is the name of the property being validated, which may be a string (the property name)
    or a ``tuple`` of strings (the property name and the namespace for the property name).

    If a ``context`` is provided, then if the top level property is being validated, and it appears inside a field
    present in the ``context`` then the ``default`` validator at the top level is overridden by the ``default`` validator
    in the ``context``.

    For example, consider the following rules:

    .. code-block:: python

        {
            Properties.TYPE: {
                "default": validate.type_checker,
                "context": {
                    Properties.ACTOR: {
                        "default": validate.one_of([
                            ActivityStreamsTypes.SERVICE,
                            ActivityStreamsTypes.APPLICATION
                        ])
                    }
                }
            }
        }

    This tells us that the ``TYPE`` property should be validated with ``validate.type_checker`` by default.  But if
    we are looking at that ``TYPE`` property inside an ``ACTOR`` object, then instead we should use ``validate.one_of``.

    When the :py:meth:`get` method is called, the ``context`` parameter can be used to specify the context in which the
    property is being validated.

    :param rules: The rules to use for validation
    """
    def __init__(self, rules: dict):
        """
        Create a new validator with the given rules

        :param rules: The rules to use for validation
        """
        self._rules = rules

    def get(self, property: Union[str, Tuple[str, str]], context: Union[str, Tuple[str, str]]=None) -> Callable:
        """
        Get the validation function for the given property in the given context

        :param property: the property to get the validation function for
        :param context: the context in which the property is being validated
        :return: a function which can be used to validate the property
        """
        default = self._rules.get(property, {}).get("default", None)
        if context is not None:
            # FIXME: down the line this might need to become recursive
            specific = self._rules.get(property, {}).get("context", {}).get(context, {}).get("default", None)
            if specific is not None:
                return specific
        return default

    def rules(self):
        """The ruleset for this validator"""
        return self._rules

    def add_rules(self, rules):
        existing = self.rules()

        def merge_dicts_recursive(dict1, dict2):
            merged = dict1.copy()  # Start with a copy of dict1
            for key, value in dict2.items():
                if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                    merged[key] = merge_dicts_recursive(merged[key], value)
                else:
                    merged[key] = value
            return merged

        self._rules = merge_dicts_recursive(existing, rules)


#############################################
## URI validator

URI_RE = r'^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?'
SCHEME = re.compile(r'^[a-zA-Z][a-zA-Z0-9+\-.]*$')
IPv6 = re.compile(r"(?:^|(?<=\s))\[{0,1}(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))]{0,1}(?=\s|$)")

HOSTPORT = re.compile(
        r'^(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
        r"(?:^|(?<=\s))(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))(?=\s|$)"
        r')' 
        r'(?::\d+)?$', # optional port
        re.IGNORECASE)

MARK = "-_.!~*'()"
UNRESERVED = "a-zA-Z0-9" + MARK
PCHARS = UNRESERVED + ":@&=+$," + "%/;"
PATH = re.compile("^/{0,1}[" + PCHARS + "]*$")

RESERVED = ";/?:@&=+$,"
URIC = RESERVED + UNRESERVED + "%"
FREE = re.compile("^[" + URIC + "]+$")

USERINFO = re.compile("^[" + UNRESERVED + "%;:&=+$,]*$")


def absolute_uri(obj, uri: str) -> bool:
    """
    Validate that the given string is an absolute URI

    :param obj: The Notify object to which the property being validated belongs.
    :param uri: The string that claims to be an absolute URI
    :return: ``True`` if the URI is valid, otherwise ValueError is raised
    """
    m = re.match(URI_RE, uri)
    if m is None:
        raise ValueError("Invalid URI")

    # URI must be absolute, so requires a scheme
    if m.group(2) is None:
        raise ValueError("URI requires a scheme (this may be a relative rather than absolute URI)")

    scheme = m.group(2)
    authority = m.group(4)
    path = m.group(5)
    query = m.group(7)
    fragment = m.group(9)

    # scheme must be alpha followed by alphanum or +, -, or .
    if scheme is not None:
        if not SCHEME.match(scheme):
            raise ValueError(f"Invalid URI scheme `{scheme}`")

    if authority is not None:
        userinfo = None
        hostport = authority
        if "@" in authority:
            userinfo, hostport = authority.split("@", 1)
        if userinfo is not None:
            if not USERINFO.match(userinfo):
                raise ValueError(f"Invalid URI authority `{authority}`")
        # determine if the domain is ipv6
        if hostport.startswith("["):    # ipv6 with an optional port
            port_separator = hostport.rfind("]:")
            port = None
            if port_separator != -1:
                port = hostport[port_separator+2:]
                host = hostport[1:port_separator]
            else:
                host = hostport[1:-1]
            if not IPv6.match(host):
                raise ValueError(f"Invalid URI authority `{authority}`")
            if port is not None:
                try:
                    int(port)
                except ValueError:
                    raise ValueError(f"Invalid URI port `{port}`")
        else:
            if not HOSTPORT.match(hostport):
                raise ValueError(f"Invalid URI authority `{authority}`")

    if path is not None:
        if not PATH.match(path):
            raise ValueError(f"Invalid URI path `{path}`")

    if query is not None:
        if not FREE.match(query):
            raise ValueError(f"Invalid URI query `{query}`")

    if fragment is not None:
        if not FREE.match(fragment):
            raise ValueError(f"Invalid URI fragment `{fragment}`")

    return True

###############################################


def url(obj, url:str) -> bool:
    """
    Validate that the given string is an absolute HTTP URI (i.e. a URL)

    :param obj: The Notify object to which the property being validated belongs.
    :param uri: The string that claims to be an HTTP URI
    :return: ``True`` if the URI is valid, otherwise ValueError is raised
    """
    absolute_uri(obj, url)
    o = urlparse(url)
    if o.scheme not in ["http", "https"]:
        raise ValueError("URL scheme must be http or https")
    if o.netloc is None or o.netloc == "":
        raise ValueError("Does not appear to be a valid URL")
    return True


def one_of(values: List[str]) -> Callable:
    """
    Closure that returns a validation function that checks that the value is one of the given values

    :param values: The list of values to choose from.  When the returned function is run, the value passed to it
        must be one of these values
    :return: a validation function
    """
    def validate(obj, x):
        if x not in values:
            raise ValueError(f"`{x}` is not one of the valid values: {values}")
        return True
    return validate

def at_least_one_of(values: List[str]) -> Callable:
    """
    Closure that returns a validation function that checks that a list of values contains at least one
    of the given values

    :param values: The list of values to choose from.  When the returned function is run, the values (plural) passed to it
        must contain at least one of these values
    :return: a validation function
    """
    def validate(obj, x):
        if not isinstance(x, list):
            x = [x]

        for entry in x:
            if entry in values:
                return True

        # if we don't find one of the document values in the list of "at least one of" values,
        # raise an exception
        raise ValueError(f"`{x}` is not one of the valid values: {values}")

    return validate

def contains(value: str) -> Callable:
    """
    Closure that returns a validation function that checks the provided values contain the required value

    :param value: The value that must be present. When the returned function is run, the value(s) passed to it
        must contain this value
    :return: a validation function
    """
    values = value
    if not isinstance(values, list):
        values = [values]
    values = set(values)

    def validate(obj, x):
        if not isinstance(x, list):
            x = [x]
        x = set(x)

        intersection = x.intersection(values)
        if intersection != values:
            raise ValueError(f"`{x}` does not contain the required value(s): {values}")
        return True

    return validate

def type_checker(obj, value):
    """
    Validate that the given value is of the correct type for the object.  The exact behaviour of this function
    depends on the object provided:

    * If the object has an ``ALLOWED_TYPES`` attribute which is not an empty list, then the value must be one of
        the types in that list
    * If the object has a ``TYPE`` attribute, then the value must be, or contain, that type
    * In all other cases, type validation will succeed

    :param obj: the notify object being validated
    :param value: the type being validated
    :return: ``True`` if the type is valid, otherwise ValueError is raised
    """
    if hasattr(obj, "ALLOWED_TYPES"):
        allowed = obj.ALLOWED_TYPES
        if len(allowed) == 0:
            return True
        validator = one_of(allowed)
        validator(obj, value)
    elif hasattr(obj, "TYPE"):
        ty = obj.TYPE
        validator = contains(ty)
        validator(obj, value)
    return True
