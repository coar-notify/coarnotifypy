"""Base class for fixture factories."""


class BaseFixtureFactory:
    """Base class for fixture factories."""

    @classmethod
    def source(cls, copy=True):
        """Return the source."""
        raise NotImplementedError()

    @classmethod
    def invalid(cls):
        """Invalid source."""
        source = cls.source()
        cls._base_invalid(source)
        return source

    @classmethod
    def expected_value(cls, path):
        """Return the expected value."""
        source = cls.source(copy=False)  # we're only reading the value, so no need to clone it
        return cls._value_from_dict(path, source)

    @classmethod
    def _base_invalid(cls, source):
        """Set the base invalid values."""
        source["id"] = "not a uri"
        source["inReplyTo"] = "not a uri"
        source["origin"]["id"] = "urn:uuid:4fb3af44-d4f8-4226-9475-2d09c2d8d9e0"
        source["origin"]["inbox"] = "not a uri"
        source["origin"]["type"] = "NotAValidType"
        source["target"]["id"] = "urn:uuid:4fb3af44-d4f8-4226-9475-2d09c2d8d9e0"
        source["target"]["inbox"] = "not a uri"
        source["target"]["type"] = "NotAValidType"
        source["type"] = "NotAValidType"
        return source

    @classmethod
    def _actor_invalid(self, source):
        """Set the actor invalid values."""
        source["actor"]["id"] = "not a uri"
        source["actor"]["type"] = "NotAValidType"
        return source

    @classmethod
    def _object_invalid(self, source):
        """Set the object invalid values."""
        source["object"]["id"] = "not a uri"
        source["object"]["cite_as"] = "urn:uuid:4fb3af44-d4f8-4226-9475-2d09c2d8d9e0"
        return source

    @classmethod
    def _context_invalid(self, source):
        """Set the context invalid values."""
        source["context"]["id"] = "not a uri"
        source["context"]["type"] = "NotAValidType"
        source["context"]["cite_as"] = "urn:uuid:4fb3af44-d4f8-4226-9475-2d09c2d8d9e0"
        return source

    @classmethod
    def _value_from_dict(cls, path, dictionary):
        """Return the value from the dictionary."""
        bits = path.split(".")
        node = dictionary
        for bit in bits:
            node = node[bit]
        return node
