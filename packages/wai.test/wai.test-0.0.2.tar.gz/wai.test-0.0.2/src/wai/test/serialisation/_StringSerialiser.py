from typing import IO, Optional

from ._RegressionSerialiser import RegressionSerialiser


class StringSerialiser(RegressionSerialiser[str]):
    """
    Basic serialiser which saves a string result in a .txt file.
    """
    @classmethod
    def binary(cls) -> bool:
        return False

    @classmethod
    def extension(cls) -> str:
        return "txt"

    @classmethod
    def serialise(cls, result: str, file: IO[str]):
        file.write(result)

    @classmethod
    def deserialise(cls, file: IO[str]) -> str:
        return file.read()

    @classmethod
    def compare(cls, result: str, reference: str) -> Optional[str]:
        if super().compare(result, reference) is not None:
            return "Result:\n" + \
                result + "\n" + \
                "Reference:\n" + \
                reference
