class RadiantVoicesError(Exception):
    pass


class ControllerValueError(RadiantVoicesError, ValueError):
    pass


class MappingOverflowError(RadiantVoicesError, OverflowError):
    pass


class EmptySynthError(RadiantVoicesError):
    pass
