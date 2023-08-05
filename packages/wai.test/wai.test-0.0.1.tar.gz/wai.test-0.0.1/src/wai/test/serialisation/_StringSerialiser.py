from typing import IO

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
