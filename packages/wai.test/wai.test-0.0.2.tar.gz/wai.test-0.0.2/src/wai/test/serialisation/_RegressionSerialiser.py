import os
from abc import abstractmethod
from typing import IO, Generic, TypeVar, AnyStr, Optional

# The types of the regression result and the disk type
ResultType = TypeVar("ResultType")


class RegressionSerialiser(Generic[ResultType]):
    """
    Base class for serialisers of regression results to/from disk. Purely
    class-based, should not need to be instantiated.
    """
    @classmethod
    @abstractmethod
    def binary(cls) -> bool:
        """
        Whether this serialiser serialises to binary or text.

        :return:    True if this serialiser class serialises to binary,
                    False if it serialises to text.
        """
        pass

    @classmethod
    @abstractmethod
    def extension(cls) -> str:
        """
        Gets the extension to use for regression files.
        """
        pass

    @classmethod
    def extend(cls, filename: str) -> str:
        """
        Adds the extension to the end of the given filename, if it's not
        already present.

        :param filename:    The filename to extend.
        :return:            The filename, with the extension.
        """
        # Get the extension with a leading dot
        dotted_extension: str = "." + cls.extension()

        # Add the extension if it's not already present
        if not filename.endswith(dotted_extension):
            filename += dotted_extension

        return filename

    @classmethod
    def exists(cls, filename: str) -> bool:
        """
        Whether a regression file exists under the given filename.

        :param filename:    The filename to look for.
        :return:            True if the given regression file exists,
                            False if not.
        """
        return os.path.exists(cls.extend(filename))

    @classmethod
    def save(cls, result: ResultType, filename: str):
        """
        Saves the given result to the given file.

        :param result:      The result to save.
        :param filename:    The name of the file to save to.
        """
        # Add the extension to the filename
        filename = cls.extend(filename)

        # If the path to the file doesn't exist, create it
        path = os.path.dirname(filename)
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

        # Determine if we need to open in binary or text mode
        mode = "w" if not cls.binary() else "wb"

        # Serialise the result to the file
        with open(filename, mode) as file:
            cls.serialise(result, file)

    @classmethod
    @abstractmethod
    def serialise(cls, result: ResultType, file: IO[AnyStr]):
        """
        Serialises the given result into the given file.

        :param result:  The result to serialise.
        :param file:    The handle to a file to write to.
        """
        pass

    @classmethod
    def load(cls, filename: str) -> ResultType:
        """
        Loads the regression result from the given file.

        :param filename:    The file to load from.
        :return:            The result stored in the file.
        """
        # Add the extension to the filename
        filename = cls.extend(filename)

        # Determine if we need to open in binary or text mode
        mode = "r" if not cls.binary() else "rb"

        # Deserialise and return the result from the file
        with open(filename, mode) as file:
            return cls.deserialise(file)

    @classmethod
    @abstractmethod
    def deserialise(cls, file: IO[AnyStr]) -> ResultType:
        """
        Deserialises a regression result from the given file.

        :param file:    The file to read from.
        :return:        The regression result stored in the file.
        """
        pass

    @classmethod
    def compare(cls, result: ResultType, reference: ResultType) -> Optional[str]:
        """
        Compares the result to the reference value for equality. Can be
        overridden to define a different sense of equality other than the
        standard == result.

        :param result:      The result of this regression test.
        :param reference:   The reference result from disk.
        :return:            A message describing why the comparison failed,
                            or None if it passed.
        """
        return "result does not equal reference" if result != reference else None
