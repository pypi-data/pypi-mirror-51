import functools

from ._Test import Test
from .. import AbstractTest


def RegressionTest(method):
    """
    Decorator which marks a class method as a regression test.
    """
    # Make the method a test
    method = Test(method)

    # Wrap the method with the regression infrastructure
    @functools.wraps(method)
    def when_called(test: AbstractTest):
        results = method(test)

        test.handle_regression_results(results)

    return when_called
