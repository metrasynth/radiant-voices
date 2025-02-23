from contextlib import contextmanager

RAISE_CONTROLLER_VALUE_ERRORS = True
"""For validation errors, True to raise an exception, False to log a warning."""

RAISE_RANGE_ERRORS_ON_READ = False
"""Whether RAISE_RANGE_ERRORS should be True when reading a file."""


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


class RadiantVoicesWarning(Warning):
    pass


class ControllerValueWarning(RadiantVoicesWarning):
    pass


def raise_or_warn_controller_value_validation(from_exc, log, *args):
    if RAISE_CONTROLLER_VALUE_ERRORS:
        raise ControllerValueError(*args) from from_exc
    log.warning(*args, exc_info=from_exc)


@contextmanager
def override_raise_controller_value_errors(new_value: bool):
    """Context manager to temporarily enable/disable raising controller value errors."""
    global RAISE_CONTROLLER_VALUE_ERRORS
    old_raise_errors = RAISE_CONTROLLER_VALUE_ERRORS
    RAISE_CONTROLLER_VALUE_ERRORS = new_value
    try:
        yield
    finally:
        RAISE_CONTROLLER_VALUE_ERRORS = old_raise_errors
