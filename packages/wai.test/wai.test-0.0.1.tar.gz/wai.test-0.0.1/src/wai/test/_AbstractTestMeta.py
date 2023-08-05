from abc import ABCMeta
from typing import Dict, Any
from unittest import defaultTestLoader

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

        return super().__new__(mcs, name, bases, namespace, **kwargs)

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
