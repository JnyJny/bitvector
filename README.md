# Bit Vectors For Humans™

This simple bit vector implementation aims to make addressing single
bits a little less fiddly. It can be used by itself to work with bit
fields in an integer word, but it really starts to shine when you use
the supplied `BitField` descriptor with a subclass of `BitVector`:

```python
> from bitvector import BitVector, BitField
>
> class IOTDeviceCommand(BitVector):
>     def __init__(self):
>         super().__init__(size=32)
>
>     power = BitField(0, 1) # offset and size
>     spin  = BitField(1, 1)
>     speed = BitField(2, 4)
>     sense = BitField(6, 2)
>     red   = BitField(8, 8)
>     blue  = BitField(16, 8)
>     green = BitField(24, 8)
>
> widget_cmd = IOTDeviceCommand()
> widget_cmd.power = 1
> widget_cmd.sense = 2
> widget_cmd.speed = 5
> widget_cmd.red = 0xaa
> widget_cmd.blue = 0xbb
> widget_cmd.green = 0xcc
> widget_cmd
IOTDeviceCommand(value=0xccbbaa95, size=32)
> widget_cmd.bytes
b'\xcc\xbb\xaa\x95'
```


## Installation

```console
$ pip install bitvector-for-humans
$ pydoc bitvector
...
```

Or directly from github:

```console
$ pip install git+https://github.com/JnyJny/bitvector.git
```

## Motivation

1. Address sub-byte bits in a less error prone way.
2. Minimize subdependencies.
3. Learn something about descriptors. 

## Caveats

The tests need expanding and I got lazy when writing the multi-bit
setting / getting code and it could undoubtedly be improved. Pull
requests gladly accepted.

## Other Ways to Implement a Bit Vector

1. Python builtin `ctypes.Structure` allows sub-byte bit fields
2. Python builtin `struct` provides extensive support for byte manipulations
3. Python3 IntEnums can be used to build bit field masks
4. The plain `int` will serve admirably with bitwise operators
5. Provide cffi bindings to existing bit-twiddling libraries
6. Use Numpy bool arrays as the "backing store"
7. Other good ideas I overlooked, forgot about or just plain don't know.






