"""Access Bits in a BitVector
"""


class BitField:
    """Data Descriptor for accessing named fields in a BitVector.

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

    def __init__(self, offset: int, width: int = 1):
        """
        :param offset: int
        :param width: int
        """
        self.field = slice(offset, offset + width)

    def __get__(self, obj, type=None) -> int:
        return obj[self.field]

    def __set__(self, obj, value) -> None:
        obj[self.field] = value

    def __set_name__(self, owner, name) -> None:
        self.name = name


class ReadOnlyBitField:
    """Experimental.
    """

    def __init__(self, offset: int, width: int = 1, default: int = None):
        self.field = slice(offset, offset + width)
        self.default = default & ((1 << width) - 1)

    def __get__(self, obj, type=None) -> int:
        value = obj[self.field]

        if self.default is None:
            return value

        if value != self.default:
            obj[self.field] = self.default
            value = self.default

        return value

    def __set__(self, obj, value) -> None:
        return

    def __set_name__(self, owner, name) -> None:
        self.name = name
