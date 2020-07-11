"""A vector of bits for Humans™!
"""

import functools
import operator

from typing import Union


@functools.total_ordering
class BitVector:
    """A Bit Vector is a list of bits in packed (integer)
    format that can be accessed by indexing into the vector
    or using a slice (via conventional square brackets 
    notation). 

    """

    @classmethod
    def zeros(cls, size: int = 128):
        """Create a BitVector initialized with zeros.
        
        :param size: int
        """

        return cls(size=size)

    @classmethod
    def ones(cls, size: int = 128):
        """Create a BitVector initialized with ones.

        :param size: int
        """

        bv = cls()
        bv.set()
        return bv

    def __init__(self, value: int = 0, size: int = 128):
        """Initialize a BitVector with integer value and size in bits.

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
        """The integer value of this BitVector.
        """
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
        """Toggle the bit at `offset` in the vector and return the previous value.
        
        :param offset: int
        :return: int
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
            retval = self.__class__(retval, size=len(self))

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
            retval = self.__class__(retval, size=len(self))
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

    def __bool__(self) -> bool:
        """Returns False if zero else True."""
        return bool(self.value)

    def __eq__(self, other) -> bool:
        """Tests equality between BitVector and other.

        :param other: Union[BitVector, int]
        :return: bool
        """
        return self.__binary_op(other, operator.eq)

    def __gt__(self, other) -> bool:
        """True if BitVector is greater than other.

        :param other: Union[BitVector, int]
        :return: bool
        """
        return self.__binary_op(other, operator.gt)

    def __add__(self, other):
        """Add BitVector to other and return a BitVector initialized with the sum.
        
        :param other: Union[BitVector|int]
        :return: BitVector
        """
        return self.__binary_op(other, operator.add, return_obj=True)

    def __radd__(self, other) -> int:
        """Add BitVector to other, returning integer value.

        :param other: int
        :return: int
        """
        return self.__binary_op(other, operator.add, reverse=True)

    def __iadd__(self, other):
        """Add `other` to self in-pace. 

        :param other: Union[BitVector, int]
        :return: self
        """
        return self.__inplace_op(other, operator.add)

    def __sub__(self, other):
        """Subtract other from self and return a BitVector intialized with the difference.

        :param other: Union[BitVector, int]
        :return: BitVector
        """
        return self.__binary_op(other, operator.sub, return_obj=True)

    def __rsub__(self, other):
        """Subtract this BitVector from an int and return the integer difference.

        :param other: int
        :return: int
        """
        return self.__binary_op(other, operator.sub, reverse=True)

    def __isub__(self, other):
        """Subtract other from this BitVector in-place.

        :param other: Union[BitVector, int]
        :return: BitVector
        """
        return self.__inplace_op(other, operator.sub)

    def __mul__(self, other):
        """Multiply BitVector with other and return a BitVector initialized with the product.

        :param other: Union[BitVector, int]
        :return: BitVector
        """
        return self.__binary_op(other, operator.mul, return_obj=True)

    def __rmul__(self, other):
        """Multiply other with the integral value of this BitVector and return an the product.

        :param other: Union[BitVector, int]
        :return: int
        """
        return self.__binary_op(other, operator.mul, reverse=True)

    def __imul__(self, other):
        """Multiply BitVector with other and update in-place. 

        :param other: Union[BitVector, int]
        :return: self
        """
        return self.__inplace_op(other, operator.mul)

    def __truediv__(self, other):
        """Divide BitVector with other and return a BitVector initialized with the quotient.
        :param other: Union[BitVector, int, float]
        :param: BitVector
        """
        return self.__binary_op(other, operator.truediv, return_obj=True)

    def __rtruediv__(self, other):
        """Divide other with BitVector and return a float quotient.
        :param other: Union[BitVector, int, float]
        :return: float
        """
        return self.__binary_op(other, operator.truediv, reverse=True)

    def __itruediv__(self, other):
        """Divide BitVector by other and update in-place.

        :param other: Union[BitVector, int]
        :return: self
        """
        return self.__inplace_op(other, operator.truediv)

    def __floordiv__(self, other):
        """Divide BitVector with other and return the a BitVector initialized with the rounded quotient.

        :param other: Union[BitVector, int, float]
        :return: BitVector
        """
        return self.__binary_op(other, operator.floordiv, return_obj=True)

    def __rfloordiv__(self, other):
        """Divide other by BitVector and return a float quotient.

        :param other: Union[int, float]
        :return: float
        """
        return self.__binary_op(other, operator.floordiv, reverse=True)

    def __ifloordiv__(self, other):
        """Divide BitVector by other and update in-place.

        :param other: Union[BitVector, int, float]
        :return: self
        """
        return self.__inplace_op(other, operator.floordiv)

    def __and__(self, other):
        """Performs a bitwise AND of BitVector with other and returns a BitVector initialized with the result.

        :param other: Union[BitVector, int]
        :return: BitVector
        """
        return self.__binary_op(other, operator.and_, return_obj=True)

    def __rand__(self, other):
        """Performs a bitwise AND of other with BitVector and returns an integer result.

        :param other: Union[BitVector, int]
        :return: int
        """
        return self.__binary_op(other, operator.and_, reverse=True)

    def __iand__(self, other):
        """Performs a bitwise AND of other with BitVector in-place.

        :param other: Union[BitVector, int]
        :return: self
        """
        return self.__inplace_op(other, operator.and_)

    def __or__(self, other):
        """Performs a bitwise OR of BitVector with other and returns a BitVector initialized with the result.

        :param other: Union[BitVector, int]
        :return: BitVector
        """
        return self.__binary_op(other, operator.or_, return_obj=True)

    def __ror__(self, other):
        """Performs a bitwise OR of other with BitVector and returns the integer result.

        :param other: Union[BitVector, int]
        :return: int
        """
        return self.__binary_op(other, operator.or_)

    def __ior__(self, other):
        """Performs a bitwise OR of other with BitVector in-place.

        :param other: Union[BitVector, int]
        :return: self
        """
        return self.__inplace_op(other, operator.or_)

    def __xor__(self, other):
        """Performs a bitwise XOR of BitVector with other and returns a BitVector initialized with the result.

        :param other: Union[BitVector, int]
        """
        return self.__binary_op(other, operator.xor, return_obj=True)

    def __rxor__(self, other):
        """Performs a bitwise XOR of other with BitVector and returns the integer result.

        :param other: Union[BitVector, int]
        :return: int
        """
        return self.__binary_op(other, operator.xor)

    def __ixor__(self, other):
        """Performs a bitwise XOR of other with BitVector in-place.

        :param other: Union[BitVector, int]
        :return: self
        """
        return self.__inplace_op(other, operator.xor)

    def __invert__(self):
        """Inverts BitVector and returns a new BitVector with the result.

        :param other: Union[BitVector, int]
        :return: BitVector
        """
        return self.__unary_op(operator.invert, return_obj=True)

    def __neg__(self):
        """Inverts BitVector and returns a new BitVector with the result.

        >>> x = -BitVector(0, size=16)
        >>> x.hex
        0xfffff

        :param other: Union[BitVector, int]
        :return: BitVector
        """
        return self.__unary_op(operator.invert, return_obj=True)

    def __pos__(self):
        """Returns a copy of this BitVector.

        :param other: Union[BitVector, int]
        """
        return self.__unary_op(operator.pos, return_obj=True)

    def __lshift__(self, other):
        """Performs a bitwise left shift of BitVector by other positions and returns
        a BitVector initialized with the results.

        :param other: Union[BitVector, int]
        :return: BitVector
        """
        return self.__binary_op(other, operator.lshift, return_obj=True)

    def __ilshift__(self, other):
        """Shifts the contents of BitVector left by other positions in-place.

        :param other: Union[BitVector, int]
        :return: self
        """
        return self.__inplace_op(other, operator.lshift)

    def __rshift__(self, other):
        """Performs a bitwise right shift of BitVector by other positions and returns
        a BitVector initialized with the results.

        :param other: Union[BitVector, int]
        :return: BitVector
        """
        return self.__binary_op(other, operator.rshift, return_obj=True)

    def __irshift__(self, other):
        """Shifts the contents of BitVector right by other positions in-place.

        :param other: Union[BitVector, int]
        :return: self
        """
        return self.__inplace_op(other, operator.rshift)
