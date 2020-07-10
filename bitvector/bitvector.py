"""A vector of bits for Humans™!
"""

import functools
import operator

from typing import Union
from loguru import logger


@functools.total_ordering
class BitVector:
    """A Bit Vector is a list of bits in packed (integer)
    format that can be accessed by indexing into the vector
    or using a slice (via conventional square brackets 
    notation). 

    """

    @classmethod
    def zeros(cls, size: int = 128):
        return cls(size=size)

    @classmethod
    def ones(cls, size: int = 128):
        bv = cls()
        bv.set()
        return bv

    def __init__(self, value: int = 0, size: int = 128):
        """
        :param value: int
        :param size: int

        Raises:
        - ValueError if size <= 0
        """
        if size <= 0:
            raise ValueError("Size must greater than zero.")

        self.MAX = (1 << size) - 1
        self.value = value

    @property
    def value(self) -> int:
        return getattr(self, "_value", 0)

    @value.setter
    def value(self, new_value: int) -> None:
        self._value = int(new_value) & self.MAX

    def clear(self):
        """Clears all bits in the vector to zero."""
        self._value = 0

    def set(self):
        """Sets all bits in the vector to one."""
        self._value = self.MAX

    def _getb(self, offset: int) -> int:
        """Retrieves the bit value at offset."""

        if offset > len(self) - 1:
            raise IndexError(offset)

        return (self.value >> offset) & 0x1

    def _setb(self, offset: int) -> None:
        """Sets the bit value at offset."""
        if offset > (len(self) - 1):
            raise IndexError(offset)

        self.value |= (1 << offset) & self.MAX

    def _clrb(self, offset: int) -> None:
        """Clears the bit value at offset."""
        self.value &= ~(1 << offset)

    def _setval(self, offset: int, value: int):
        if value:
            self._setb(offset)
        else:
            self._clrb(offset)

    def toggle(self, offset: int) -> int:
        """Toggle the bit at offset in the vector and return the previous value.
        """
        prev = self._getb(offset)
        self.value ^= (1 << offset) & self.MAX
        return prev

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self!s}, size={len(self)})"

    def __str__(self) -> str:
        nibbles = (len(self) // 4) + 1 if (len(self) % 4) else 0
        hexstr = "0x{{:0{0}x}}".format(nibbles)
        return hexstr.format(self.value)

    def __len__(self) -> int:
        """Length of the vector in bits."""
        try:
            return self._len
        except AttributeError:
            pass
        self._len = self.MAX.bit_length()
        return self._len

    def __getitem__(self, key: Union[int, slice]) -> int:
        """Given a key, retrieve a bit or bitfield."""
        try:
            if key < 0:
                key += len(self)
            return self._getb(key)
        except TypeError:
            pass

        try:
            value = 0
            for n, b in enumerate(range(*key.indices(len(self)))):
                v = self._getb(b)
                if v:
                    value += 1 << n
            return value
        except AttributeError:
            raise ValueError(f"Unknown key type: {type(key)}")

    def __setitem__(self, key: Union[int, slice], value: Union[int, bool]) -> None:
        """Given a key, set a bit or bitfield to the supplied value.

        If value is True or False and the key is a slice describing a
        bit field, each bit in the field takes on the value.  Otherwise,
        the value is left shifted and the lsb is added to the next offset
        in the bit field.

        > b[:8] = True   # results in bit0:bit7 == 0b11111111
        > b[:8] = 0x1    # results in bit0:bit7 == 0b00000001
        
        The difference is subtle and perhaps should not be considered a feature.

        Supports negative indexing.
        """
        try:
            if key < 0:
                key += len(self)

            self._setval(key, value)
            return

        except TypeError:
            pass

        try:
            if value is True or value is False:
                for b in range(*key.indices(len(self))):
                    self._setval(b, value)
                return

            for n, b in enumerate(range(*key.indices(len(self)))):
                self._setval(b, (value >> n) & 0x1)

        except AttributeError:
            raise ValueError("Expected int or slice key") from None

    def __binary_op(self, other, func, return_obj: bool = False, reverse: bool = False):
        """Calls the supplied function `func` with self and other.

        If the user sets return_obj to True, a new BitVector initialized with the
        results of `func` is returned. Otherwise the return type is assumed to be
        `int`.  

        :param other: Union[int, BitVector]
        :param func: callable from operator
        :param return_obj: bool
        :return: Union[int, bool, BitVector]
        """

        logger.debug(f"{self} {other} {func} {return_obj} {reverse}")

        try:
            retval = func(self.value, other.value)
            if return_obj:
                size = len(min(self, other, key=len))
                retval = self.__class__(retval, size=size)
            return retval
        except AttributeError:
            pass

        if reverse:
            return func(other, self.value)

        retval = func(self.value, other)

        if return_obj:
            retval = self.__class__(retval)

        return retval

    def __unary_op(self, func, return_obj: bool = False):
        """Calls the supplied function `func` with self and returns the result.

        If return_obj is True, the return value is a BitVector initialized from
        the results of `func`. 

        :param func: callable from operator 
        :param return_obj: bool
        :return: Union[int, BitVector]
        """

        retval = func(self.value) & self.MAX
        if return_obj:
            retval = self.__class__(retval)
        return retval

    def __inplace_op(self, other, func) -> object:
        """Calls the supplied binary function `func` with self and other
        and updates self with the results. 

        :param other:  Union[int, BitVector]
        :param func: Callable from operator
        :return: self
        """
        try:
            self.value = func(self.value, other.value)
        except AttributeError:
            self.value = func(self.value, other)
        return self

    @property
    def bin(self) -> str:
        """Binary string representation of BitVector."""
        return f"0b{bin(self.value)[2:].zfill(len(self))}"

    @property
    def hex(self) -> str:
        """Hexadecimal string representation of BitVector."""
        return hex(self.value)

    @property
    def bytes(self) -> bytes:
        """Byte array representation of BitVector."""
        n = len(self) // 8 + (1 if len(self) % 8 else 0)
        return self.value.to_bytes(n, "big")

    def __bool__(self):
        return bool(self.value)

    __eq__ = functools.partialmethod(__binary_op, func=operator.eq)
    __gt__ = functools.partialmethod(__binary_op, func=operator.gt)

    __add__ = functools.partialmethod(__binary_op, func=operator.add, return_obj=True)
    __radd__ = functools.partialmethod(__binary_op, func=operator.add, reverse=True)
    __iadd__ = functools.partialmethod(__inplace_op, func=operator.add)

    __sub__ = functools.partialmethod(__binary_op, func=operator.sub, return_obj=True)
    __rsub__ = functools.partialmethod(__binary_op, func=operator.sub, reverse=True)
    __isub__ = functools.partialmethod(__inplace_op, func=operator.sub)

    __mul__ = functools.partialmethod(__binary_op, func=operator.mul, return_obj=True)
    __rmul__ = functools.partialmethod(__binary_op, func=operator.mul, reverse=True)
    __imul__ = functools.partialmethod(__inplace_op, func=operator.mul)

    __truediv__ = functools.partialmethod(
        __binary_op, func=operator.truediv, return_obj=True
    )
    __rtruediv__ = functools.partialmethod(
        __binary_op, func=operator.truediv, reverse=True
    )
    __itruediv__ = functools.partialmethod(__inplace_op, func=operator.truediv)

    __floordiv__ = functools.partialmethod(
        __binary_op, func=operator.floordiv, return_obj=True
    )
    __rfloordiv__ = functools.partialmethod(
        __binary_op, func=operator.floordiv, reverse=True
    )
    __ifloordiv__ = functools.partialmethod(__inplace_op, func=operator.floordiv)

    __and__ = functools.partialmethod(__binary_op, func=operator.and_, return_obj=True)
    __rand__ = functools.partialmethod(__binary_op, func=operator.and_, reverse=True)
    __iand__ = functools.partialmethod(__inplace_op, func=operator.and_)

    __or__ = functools.partialmethod(__binary_op, func=operator.or_, return_obj=True)
    __ror__ = functools.partialmethod(__binary_op, func=operator.or_)
    __ior__ = functools.partialmethod(__inplace_op, func=operator.or_)

    __xor__ = functools.partialmethod(__binary_op, func=operator.xor, return_obj=True)
    __rxor__ = functools.partialmethod(__binary_op, func=operator.xor)
    __ixor__ = functools.partialmethod(__inplace_op, func=operator.xor)

    __invert__ = functools.partialmethod(__unary_op, operator.invert, return_obj=True)
    __neg__ = functools.partialmethod(__unary_op, operator.invert, return_obj=True)

    __pos__ = functools.partialmethod(__unary_op, operator.pos, return_obj=True)

    __lshift__ = functools.partialmethod(
        __binary_op, func=operator.lshift, return_obj=True
    )
    __ilshift__ = functools.partialmethod(__inplace_op, func=operator.lshift)

    __rshift__ = functools.partialmethod(
        __binary_op, func=operator.rshift, return_obj=True
    )
    __irshift__ = functools.partialmethod(__inplace_op, func=operator.rshift)
