import functools
from typing import Type

from ._Test import Test
from .. import AbstractTest


def ExceptionTest(*exceptions: Type[Exception]):
    """
    Decorator that specifies a test that should raise one
    of the given exception classes.

    :param exceptions:  The exceptions, one of which should be raised.
    """
    def applicator(method):
        # Make the method a test
        method = Test(method)

        # Wrap the method with the exception infrastructure
        @functools.wraps(method)
        def when_called(test: AbstractTest):
            with test.assertRaises(exceptions):
                return method(test)

        return when_called

    return applicator
