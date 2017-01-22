class RadiantVoicesError(Exception):
    pass


class ControllerValueError(RadiantVoicesError, ValueError):
    pass


class MappingError(RadiantVoicesError, ValueError):
    pass


class EmptySynthError(RadiantVoicesError):
    pass
