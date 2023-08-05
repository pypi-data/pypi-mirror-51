from typing import Type

from ..serialisation import RegressionSerialiser
from .._constants import SERIALISERS_ATTRIBUTE
from .._functions import get_serialisers


def WithSerialiser(result_type: Type, serialiser: Type[RegressionSerialiser]):
    """
    Decorator for regression tests which tells it to use the given
    serialiser for results of the given type.

    :param result_type:     The type of result the serialiser should be used for.
    :param serialiser:      The serialiser.
    """
    def applicator(method):
        serialisers = get_serialisers(method)

        serialisers.update({
            result_type: serialiser
        })

        setattr(method, SERIALISERS_ATTRIBUTE, serialisers)

        return method

    return applicator
