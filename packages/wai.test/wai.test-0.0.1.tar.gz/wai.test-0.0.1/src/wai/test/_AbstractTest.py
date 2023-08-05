import inspect
import os
from abc import abstractmethod
from typing import Any, Dict, Tuple, Optional, Type
from unittest import TestCase

from ._AbstractTestMeta import AbstractTestMeta
from .serialisation import BytesSerialiser, StringSerialiser, RegressionSerialiser
from ._functions import get_subject_args, get_skip_reason, get_serialisers, is_test

# The default location to store regression test results
DEFAULT_REGRESSION_ROOT = os.path.join(".", "resources", "regression")


class AbstractTest(TestCase, metaclass=AbstractTestMeta):
    def __init__(self, methodName='runTest'):
        # Get the method this instance is testing
        method = getattr(self, methodName)

        # If it's a marked test, it may have been given a
        # prefix, so substitute the base method's name
        if is_test(method):
            methodName = method.__name__

        super().__init__(methodName)

    @classmethod
    @abstractmethod
    def subject_type(cls):
        """
        Defines the subject callable for this test case.
        """
        pass

    @classmethod
    def common_resources(cls) -> Optional[Tuple[Any, ...]]:
        """
        Loads the common resources for all tests in this class.
        By default there are no common resources.
        """
        return None

    @classmethod
    def common_serialisers(cls) -> Optional[Dict[Type, Type[RegressionSerialiser]]]:
        """
        Defines additional common serialisers to use for regression
        tests in this class (in addition to the basic string and bytes
        serialisers, although these can be overridden).
        """
        return None

    @classmethod
    def common_arguments(cls) -> Optional[Tuple[Tuple[Any, ...], Dict[str, Any]]]:
        """
        Defines the default arguments to pass to the subject on instantiation.
        By default, no arguments are passed.
        """
        return None

    def setUp(self) -> None:
        # Get the method being tested
        test_method = self.get_test_method()

        # If the method is marked with skip, skip it
        skip_reason = get_skip_reason(test_method)
        if skip_reason is not None:
            self.skipTest(skip_reason)

    @classmethod
    def instantiate_subject(cls, *args, **kwargs) -> Any:
        """
        Instantiates a test subject with the given arguments.
        """
        return cls.subject_type()(*args, **kwargs)

    def subject(self) -> Any:
        # Get the arguments to use to create the test subject from the test method
        subject_args = get_subject_args(self.get_test_method())

        # If there are arguments, use them
        if subject_args is not None:
            return self.instantiate_subject(*subject_args[0], **subject_args[1])

        # If not, try using the default arguments
        subject_args = self.common_arguments()

        # If there are default arguments, use them
        if subject_args is not None:
            return self.instantiate_subject(*subject_args[0], **subject_args[1])

        # Otherwise use the default constructor
        return self.instantiate_subject()

    def handle_regression_results(self, results):
        """
        Handles comparing the results of a regression test to
        the results stored in the regression files.

        :param results:     The results of the regression test.
        """
        # Make sure the regression results are a named map
        if not isinstance(results, dict) or not all(isinstance(key, str) for key in results):
            self.fail("Regression test '" +
                      self.get_test_method_name() +
                      "' didn't return a named map of regression results")

        # Handle each result individually
        for name, result in results.items():
            self.handle_regression_result(name, result)

    def handle_regression_result(self, name: str, result: Any):
        """
        Handles the comparison of an individual regression result
        to the stored reference.

        :param name:    The name of the regression to use.
        :param result:  The result of the regression test.
        """
        # Treat each individual regression result as a sub-test
        with self.subTest(regression=name):
            # Get the serialisers for this test method
            serialisers = self.get_serialisers()

            # Get the preference order of serialiser types
            mro = inspect.getmro(type(result))

            # Get a serialiser for this result type
            serialiser = None
            for result_type in mro:
                if result_type in serialisers:
                    serialiser = serialisers[result_type]
                    break

            # Make sure we have a serialiser
            if serialiser is None:
                self.fail("No regression serialiser found for result of type: " + type(result).__name__)

            # Complete the file path for this result
            filename: str = os.path.join(self.get_regression_path(), self.get_test_method_name(), name)

            # If the regression file doesn't exist yet, create it
            if not serialiser.exists(filename):
                serialiser.save(result, filename)

            # Otherwise load and check the saved result
            else:
                reference = serialiser.load(filename)

                # Use the serialiser's notion of equality
                self.assertTrue(serialiser.compare(result, reference),
                                "Result did not equal regression reference under serialiser " +
                                serialiser.__name__)

    @classmethod
    def get_regression_root_path(cls) -> str:
        """
        Gets the path to the root directory to store regression results in.
        Can be overridden for a custom directory per test-class.

        :return:    The path to the root directory.
        """
        return DEFAULT_REGRESSION_ROOT

    @classmethod
    def get_regression_path(cls) -> str:
        """
        Gets the path to the regression results for this test-class.

        :return:    The path.
        """
        return os.path.join(cls.get_regression_root_path(), cls.get_relative_regression_path())

    @classmethod
    def get_relative_regression_path(cls) -> str:
        """
        Gets the path to the regression results for this test-class,
        relative to the root path.

        :return:    The path.
        """
        # Get the fully-qualified name of the subject (in dotted form)
        fully_qualified_name: str = cls.subject_type().__module__ + '.' + cls.subject_type().__qualname__

        # Replace the dots with platform-dependent slashes
        return fully_qualified_name.replace(".", os.sep)

    def get_serialisers(self) -> Dict[Type, Type[RegressionSerialiser]]:
        """
        Gets the serialisers to use for this test method.

        :return:    The map from type to serialiser.
        """
        # Define the basic serialisers
        serialisers = {
            str: StringSerialiser,
            bytes: BytesSerialiser
        }

        # Add the common serialisers for this class
        common_serialisers = self.common_serialisers()
        if common_serialisers is not None:
            serialisers.update(common_serialisers)

        # Override with any test-specific serialisers
        serialisers.update(get_serialisers(self.get_test_method()))

        return serialisers

    def get_test_method(self):
        """
        Gets the test method being tested by this test instance.

        :return:    The test method.
        """
        return getattr(self, self.get_test_method_name())

    def get_test_method_name(self) -> str:
        """
        Gets the name of the test method being tested by this test instance.

        :return:    The name of the test method.
        """
        return self._testMethodName
