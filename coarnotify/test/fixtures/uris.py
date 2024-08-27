from copy import deepcopy


class URIFixtureFactory:
    @classmethod
    def generate(cls, schemes=None, hosts=None, ports=None, paths=None, queries=None, fragments=None):
        schemes = schemes if schemes is not None else deepcopy(DEFAULT_SCHEMES)
        hosts = hosts if hosts is not None else deepcopy(DEFAULT_HOSTS)
        ports = ports if ports is not None else deepcopy(DEFAULT_PORTS)
        paths = paths if paths is not None else deepcopy(DEFAULT_PATHS)
        queries = queries if queries is not None else deepcopy(DEFAULT_QUERIES)
        fragments = fragments if fragments is not None else deepcopy(DEFAULT_FRAGMENTS)

        uris = []
        for scheme in schemes:
            for host in hosts:
                for port in ports:
                    for path in paths:
                        for query in queries:
                            for fragment in fragments:
                                uris.append(cls.generate_uri(scheme, host, port, path, query, fragment))

        return uris

    @classmethod
    def generate_uri(cls, scheme, host, port, path, query, fragment):
        # account for port numbers and IPv6 addresses
        if host is not None and ":" in host and port is not None and port != "":
            host = f"[{host}]"
        url = scheme + "://" if scheme is not None and scheme != "" else ""
        url += host if host is not None else ""
        url += ":" + port if port is not None and port != "" else ""
        url += path if path is not None else ""
        url += "?" + query if query is not None and query != "" else ""
        url += "#" + fragment if fragment is not None and fragment != "" else ""
        return url


DEFAULT_SCHEMES = [
    "http",
    "https"
]

DEFAULT_HOSTS = [
    "example.com",
    "localhost",
    "192.168.0.1",
    "2001:db8::7"
]

DEFAULT_PORTS = [
    "",
    "80",
    "8080"
]

DEFAULT_PATHS = [
    "",
    "/",
    "/path",
    "/path/to/file"
]

DEFAULT_QUERIES = [
    "",
    "query",
    "query=string&o=1",
]

DEFAULT_FRAGMENTS = [
    "",
    "fragment"
]