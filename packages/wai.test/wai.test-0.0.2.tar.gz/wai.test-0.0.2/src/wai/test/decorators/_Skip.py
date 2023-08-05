from .._constants import SKIP_ATTRIBUTE


def Skip(reason: str, condition: bool = True):
    """
    Decorator which marks a test as skipped.

    :param reason:      The reason the test was skipped.
    :param condition:   The condition under which to skip the test.
    """
    def applicator(method):
        if condition:
            setattr(method, SKIP_ATTRIBUTE, reason)

        return method

    return applicator
