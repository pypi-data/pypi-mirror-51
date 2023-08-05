from unittest import expectedFailure


def ExpectedFailure(method):
    """
    Decorator that marks a test method as being expected to fail.

    :param method:  The test method to mark.
    """
    return expectedFailure(method)
