class AndersenException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ConfigParseException(AndersenException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class InvalidLoggerKeyException(AndersenException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class RepeatedInitException(AndersenException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
