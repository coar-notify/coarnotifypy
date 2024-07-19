class NotifyException(Exception):
    pass


class ValidationError(NotifyException):
    def __init__(self, errors: dict=None):
        super().__init__()
        self._errors = errors if errors is not None else {}

    @property
    def errors(self):
        return self._errors

    def add_error(self, key, value):
        if key not in self._errors:
            self._errors[key] = {"errors": []}
        self._errors[key]["errors"].append(value)

    def add_nested_errors(self, key, subve: "ValidationError"):
        if key not in self._errors:
            self._errors[key] = {"errors": []}
        if "nested" not in self._errors[key]:
            self._errors[key]["nested"] = {}

        for k, v in subve.errors.items():
            self._errors[key]["nested"][k] = v

    def has_errors(self):
        return len(self._errors) > 0