"""Access Bits in a BitVector
"""


class ReadOnlyBitField:
    """Read-only data descriptor for accessing named fields in a BitVector.
    """

    def __init__(self, offset: int, width: int = 1):
        """
        :param offset: int
        :param width: int
        """
        self.field = slice(offset, offset + width)

    def __set__(self, obj, value) -> None:
        raise TypeError(f"Read-only field '{self.name}'")

    def __get__(self, obj, type=None) -> int:
        return obj[self.field]

    def __set_name__(self, owner, name) -> None:
        self.name = name


class BitField(ReadOnlyBitField):
    """Data descriptor for accessing named fields in a BitVector.

    ```python
    > from bitvector import BitVector, BitField
    >
    > class MyBV(BitVector):
    >     byte0 = BitField(0, 8)
    >     byte1 = BitField(8, 8)
    >     bit16 = BitField(16)
    >     bit17 = BitField(17)
    >     pad0  = BitField(18, 4)
    >     byte3 = BitField(32, 8)
    >
    > mybv = MyBV()
    > mybv.byte0 = 0xff
    > mybv.bit17 = 1
    > mybv.byte3 = 0x55
    > mybv
    MyBV(value=0x5502ff, length=128)
    ```
    """

    def __set__(self, obj, value) -> None:
        obj[self.field] = value
