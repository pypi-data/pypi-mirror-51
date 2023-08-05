from .._constants import SUBJECT_ARGS_ATTRIBUTE


def SubjectArgs(*args, **kwargs):
    """
    Decorator that overrides the default arguments to the subject
    initialiser.

    :param args:        The positional arguments to the subject initialiser.
    :param kwargs:      The keyword arguments to the subject initialiser.
    """
    def applicator(method):
        setattr(method, SUBJECT_ARGS_ATTRIBUTE, (args, kwargs))

        return method

    return applicator
