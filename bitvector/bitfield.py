"""Access Bits in a BitVector
"""


class BitField:
    """Data Descriptor for accessing named fields in a BitVector.
    from bitvector import BitVector, BitField

    class MyBV(BitVector):
        ...
        byte0 = BitField(0, 8)
        byte1 = BitField(8, 8)
        bit16 = BitField(16)
        bit17 = BitField(17)
        pad0  = BitField(18, 4)
        byte3 = BitField(32, 8)
    
    > mybv = MyBV()
    > mybv.byte0 = 0xff
    > mybv.bit17 = 1
    > mybv.byte3 = 0x55
    > mybv
    MyBV(value=0x5502ff, length=128)

    """

    def __init__(self, offset: int, width: int = 1):
        """
        :param offset: int
        :param width: int
        """
        self.field = slice(offset, offset + width)

    def __get__(self, obj, type=None) -> int:

        value = obj[self.field]
        return value

    def __set__(self, obj, value) -> None:
        prev = obj[self.field]
        obj[self.field] = value

    def __set_name__(self, owner, name) -> None:
        self.name = name
