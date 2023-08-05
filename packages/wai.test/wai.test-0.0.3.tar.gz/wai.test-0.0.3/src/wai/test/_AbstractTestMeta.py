from abc import ABCMeta
from typing import Dict, Any, Tuple
from unittest import defaultTestLoader, TestCase

from ._functions import is_test

# The method name prefix that unittest looks for when discovering tests
PREFIX: str = defaultTestLoader.testMethodPrefix


class AbstractTestMeta(ABCMeta):
    """
    Meta-class for test classes which allows unittest to discover
    methods marked with one of the test decorators.
    """
    def __new__(mcs, name, bases, namespace, **kwargs):
        # Make sure the test methods get picked up by unittest
        mcs.ensure_tests(namespace)

        # Make sure abstract test classes aren't instantiated by unittest
        bases = mcs.augment_bases(bases, namespace)

        return super().__new__(mcs, name, bases, namespace, **kwargs)

    @staticmethod
    def augment_bases(bases: Tuple, namespace: Dict) -> Tuple:
        """
        Augments the base classes for the new class with the TestCase class.

        :param bases:       The proposed bases for the class.
        :param namespace:   The namespace of the class.
        :return:            The base classes augmented with the TestCase class.
        """
        if not will_be_abstract(bases, namespace):
            if TestCase not in bases:
                return (*bases, TestCase)
            else:
                return bases
        else:
            if TestCase in bases:
                return tuple(base for base in bases if base is not TestCase)
            else:
                return bases

    @staticmethod
    def ensure_tests(namespace: Dict[str, Any]):
        """
        Makes sure that all methods marked with the test tag will be picked up by unittest.

        :param namespace:   The namespace of the new class.
        :return:            The namespace augmented with the unit-test methods.
        """
        # Required so namespace doesn't change during iteration
        new_attributes = {}

        # Check all attributes in the namespace
        for name, attribute in namespace.items():
            if is_test(attribute) and not name.startswith(PREFIX):
                # Create the prefixed name for the test
                test_name = PREFIX + name

                # If there is already an attribute with that name, it's fatal
                if test_name in namespace:
                    raise NameError("Test method '" +
                                    name +
                                    "' clashes with a pre-existing method '" +
                                    test_name +
                                    "'")

                # Add the prefixed name to the namespace
                new_attributes[test_name] = attribute

        # Add the prefixed names to the class attribute namespace
        namespace.update(new_attributes)


# The following code was copied here from wai.common, as we can't
# create a dependency on wai.common without creating a dependency
# cycle (wai.common depends on wai.test for testing).


def get_abstract_methods(bases: Tuple, namespace: Dict[str, Any]):
    """
    Gets the names of the abstract methods that will result from
    a class created with the given base-class set and namespace.

    :param bases:       The base-class set.
    :param namespace:   The namespace.
    :return:            The set of abstract method names.
    """
    abstract_methods = set()

    for base in bases:
        abstract_methods.update(getattr(base, '__abstractmethods__', set()))

    for name, value in namespace.items():
        if is_abstract_function(value):
            abstract_methods.add(name)
        else:
            if name in abstract_methods:
                abstract_methods.remove(name)

    return abstract_methods


def will_be_abstract(bases: Tuple, namespace: Dict[str, Any]):
    """
    Determines if a class made with the given set of base-classes
    and namespace will be abstract or concrete.

    :param bases:       The set of base classes.
    :param namespace:   The namespace of the new class.
    :return:            True if the newly-created class will be abstract,
                        False if it will be concrete.
    """
    return len(get_abstract_methods(bases, namespace)) > 0


def is_abstract_function(func):
    """
    Whether the given function is abstract in its class.

    :param func:    The function to check.
    :return:        True if the function is abstract,
                    False if not.
    """
    return getattr(func, '__isabstractmethod__', False)
