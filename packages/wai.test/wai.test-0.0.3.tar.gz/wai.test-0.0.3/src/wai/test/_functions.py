"""
Module for helper functions.
"""
from typing import Any, Dict, Tuple, Optional, Type

from .serialisation import RegressionSerialiser
from . import _constants


def is_test(method) -> bool:
    """
    Checks if the given method is a test method.

    :param method:  The method to check.
    :return:        True if the method is a test method,
                    False if not.
    """
    return getattr(method, _constants.IS_TEST_ATTRIBUTE, False)


def get_skip_reason(method) -> Optional[str]:
    """
    Checks if the given test method should be skipped.

    :param method:  The test method to check.
    :return:        The reason the test was skipped if it was,
                    or None if it wasn't.
    """
    return getattr(method, _constants.SKIP_ATTRIBUTE, None)


def get_subject_args(method) -> Optional[Tuple[Tuple[Any, ...], Dict[str, Any]]]:
    """
    Gets the arguments for the subject initialiser from the given
    method, if any.

    :param method:  The test method to get the arguments from.
    :return:        The arguments, or None if none specified.
    """
    return getattr(method, _constants.SUBJECT_ARGS_ATTRIBUTE, None)


def get_serialisers(method) -> Dict[Type, Type[RegressionSerialiser]]:
    """
    Gets the serialisers for the given test method.

    :param method:  The test method.
    :return:        The mapping from result type to serialiser.
    """
    return getattr(method, _constants.SERIALISERS_ATTRIBUTE, {})
