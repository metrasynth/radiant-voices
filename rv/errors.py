class RadiantVoicesError(Exception):
    pass


class ControllerValueError(RadiantVoicesError, ValueError):
    pass


class MappingError(RadiantVoicesError, ValueError):
    pass


class RangeValidationError(RadiantVoicesError):
    pass


class EmptySynthError(RadiantVoicesError):
    pass


class ModuleOwnershipError(RadiantVoicesError):
    pass


class PatternOwnershipError(RadiantVoicesError):
    pass
