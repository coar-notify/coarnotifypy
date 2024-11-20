"""
Module for custom exceptions
"""

class NotifyException(Exception):
    """
    Base class for all exceptions in the coarnotifypy library
    """
    pass


class ValidationError(NotifyException):
    """
    Exception class for validation errors.

    :param errors: a dictionary of errors to construct the exception around.  See below for the details
        of its structure

    This class is designed to be thrown and caught and to collect validation errors
    as it passed through the validation pipeline.

    For example an object validator may do something like this:

    .. code-block:: python

        def validate():
            ve = ValidationError()
            ve.add_error(prop_name, validate.REQUIRED_MESSAGE.format(x=pn))
            if ve.has_errors():
                raise ve
            return True

    If this is called by a subclass which is also validating, then this may be used
    like this:

    .. code-block:: python

        def validate():
            ve = ValidationError()
            try:
                super(ClassName, self).validate()
            except ValidationError as superve:
                ve = superve

            ve.add_error(prop_name, validate.REQUIRED_MESSAGE.format(x=pn))
            if ve.has_errors():
                raise ve
            return True

    By the time the ValidationError is finally raised to the top, it will contain
    all the validation errors from the various levels of validation that have been
    performed.

    The errors are stored as a multi-level dictionary with the keys at the top level
    being the fields in the data structure which have errors, and within the value
    for each key there are two possible keys:

    * errors: a list of error messages for this field
    * nested: a dictionary of further errors for nested fields

    .. code-block:: python

        {
            "key1": {
                "errors": ["error1", "error2"],
                "nested: {
                    "key2": {
                        errors: ["error3"]
                    }
                }
            }
        }

    """
    def __init__(self, errors: dict=None):
        super().__init__()
        self._errors = errors if errors is not None else {}

    @property
    def errors(self) -> dict:
        """The dictionary of errors"""
        return self._errors

    def add_error(self, key: str, value: str):
        """
        Record an error on the supplied ``key`` with the message ``value``

        :param key: the key for which an error is to be recorded
        :param value:   the error message
        :return:
        """
        if key not in self._errors:
            self._errors[key] = {"errors": []}
        self._errors[key]["errors"].append(value)

    def add_nested_errors(self, key: str, subve: "ValidationError"):
        """
        Take an existing ValidationError and add it as a nested set of errors under the supplied key

        :param key: the key under which all the nested validation errors should go
        :param subve: the existing ValidationError object
        :return:
        """
        if key not in self._errors:
            self._errors[key] = {"errors": []}
        if "nested" not in self._errors[key]:
            self._errors[key]["nested"] = {}

        for k, v in subve.errors.items():
            self._errors[key]["nested"][k] = v

    def has_errors(self) -> bool:
        """Are there any errors registered"""
        return len(self._errors) > 0

    def __str__(self):
        return str(self._errors)