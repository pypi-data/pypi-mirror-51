from typing import IO

from ._RegressionSerialiser import RegressionSerialiser


class BytesSerialiser(RegressionSerialiser[bytes]):
    """
    Basic serialiser which saves a bytes result in a .bin file.
    """
    @classmethod
    def binary(cls) -> bool:
        return True

    @classmethod
    def extension(cls) -> str:
        return "bin"

    @classmethod
    def serialise(cls, result: bytes, file: IO[bytes]):
        file.write(result)

    @classmethod
    def deserialise(cls, file: IO[bytes]) -> bytes:
        return file.read()
