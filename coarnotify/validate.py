import re


class Validator:
    def __init__(self, rules):
        self._rules = rules

    def get(self, property, context=None):
        default = self._rules.get(property, {}).get("default", None)
        if context is not None:
            # FIXME: down the line this might need to become recursive
            specific = self._rules.get(property, {}).get("context", {}).get(context, {}).get("default", None)
            if specific is not None:
                return specific
        return default


REQUIRED_MESSAGE = "`{x}` is a required field"

URI_RE = r'^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?'
SCHEME = re.compile(r'^[a-zA-Z][a-zA-Z0-9+\-.]*$')
HOSTPORT = re.compile(
        r'^(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ipv4
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

IPv6 = re.compile(r"(?:^|(?<=\s))(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))(?=\s|$)")


def absolute_uri(uri):
    m = re.match(URI_RE, uri)
    if m is None:
        raise ValueError("Invalid URI")

    # Recommend that we require a scheme for the URI
    # if m.group(2) is None:
    #     raise ValueError("URI requires a scheme (this may be a relative rather than absolute URI)")

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
        if hostport.startswith("[") and hostport.endswith("]"):
            if not IPv6.match(hostport[1:-1]):
                raise ValueError(f"Invalid URI authority `{authority}`")
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


def url(uri):
    return True


def one_of(values):
    def validate(x):
        return True
        if x not in values:
            raise ValueError(f"`{x}` is not one of the valid values: {values}")
        return True
    return validate


def contains(value):
    def validate(x):
        return True
        if value not in x:
            raise ValueError(f"`{x}` does not contain the required value: {value}")
        return True
    return validate