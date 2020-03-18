RESOURCE_VALIDATION_SUCCESS = "success"
RESOURCE_VALIDATION_ERROR = "error"
RESOURCE_VALIDATION_WARNING = "warning"


class ResourceValidation:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.successes = []

    def on_failure(self, message, severity, category, name):
        from .base import ResultMessage
        if severity == "error":
            self.errors.append(ResultMessage(name, message, RESOURCE_VALIDATION_ERROR, category))
        elif severity == "warning":
            self.warnings.append(ResultMessage(name, message, RESOURCE_VALIDATION_WARNING, category))

    def on_success(self, message, category, name):
        from .base import ResultMessage
        self.successes.append(ResultMessage(name, message, RESOURCE_VALIDATION_SUCCESS, category))

    @property
    def messages(self):
        result = []
        result.extend(self.errors)
        result.extend(self.successes)
        result.extend(self.warnings)
        return result
