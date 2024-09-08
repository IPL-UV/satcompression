import lzma
import math
import struct
from io import BytesIO


def encode_uint8(number: int) -> bytes:
    return number.to_bytes(1, byteorder="little", signed=False)


def decode_uint8(data: bytes) -> int:
    return int.from_bytes(data, byteorder="little", signed=False)


def encode_uint16(number: int) -> bytes:
    return number.to_bytes(2, byteorder="little", signed=False)


def decode_uint16(data: bytes) -> int:
    return int.from_bytes(data, byteorder="little", signed=False)


def encode_uint32(number: int) -> bytes:
    return number.to_bytes(4, byteorder="little", signed=False)


def decode_uint32(data: bytes) -> int:
    return int.from_bytes(data, byteorder="little", signed=False)


def encode_float(number: float) -> bytes:
    return struct.pack("<f", number)


def decode_float(data: bytes) -> float:
    return struct.unpack("<f", data)[0]


def encode_bitset(boolean_flags: list, stream: BytesIO):
    # Encode the number of booleans
    stream.write(encode_uint32(len(boolean_flags)))

    # Encode the booleans
    # As each boolean only needs one bit, 8 booleans can be densely packed into a single byte.
    byte_count = math.ceil(len(boolean_flags) / 8)
    for byte_index in range(byte_count):
        byte = 0

        for bit_index in range(8):
            list_index = byte_index * 8 + bit_index
            if list_index >= len(boolean_flags) or not boolean_flags[list_index]:
                continue
            # Fill the byte from left to right
            byte |= 1 << bit_index

        stream.write(encode_uint8(byte))


def decode_bitset(stream: BytesIO) -> list:
    flag_count = decode_uint32(stream.read(4))
    boolean_flags = []

    byte_count = math.ceil(flag_count / 8)
    for byte_index in range(byte_count):
        byte = decode_uint8(stream.read(1))

        for bit_index in range(8):
            list_index = byte_index * 8 + bit_index
            if list_index >= flag_count:
                continue

            boolean_flags.append((byte & (1 << bit_index)) > 0)

    return boolean_flags


def encode_image_data(
    width: int, height: int, subdivided_flags: list, colors: list, dtype: type = "uint8"
) -> bytes:
    stream = BytesIO()
    # Encode the image dimensions.
    stream.write(encode_uint32(width))
    stream.write(encode_uint32(height))

    # Encode the is_subdivided flags.
    encode_bitset(subdivided_flags, stream)

    # Encode the colors.
    for color in colors:
        for band in color.tolist():
            if dtype.name == "uint8":
                stream.write(encode_uint8(band))
            elif dtype.name == "uint16":
                stream.write(encode_uint16(band))
            elif dtype.name == "uint32":
                stream.write(encode_uint32(band))
            elif dtype.name.startswith("float"):
                stream.write(encode_float(band))
            else:
                raise ValueError(f"Unsupported dtype: {dtype}")

    blob = stream.getvalue()
    return lzma.compress(blob)


def decode_image_data(
    compressed: bytes, dtype: type = "uint8", nchannels: int = 13
) -> tuple:
    stream = BytesIO(lzma.decompress(compressed))

    width = decode_uint32(stream.read(4))
    height = decode_uint32(stream.read(4))

    subdivided_flags = decode_bitset(stream)

    # Only the leaf nodes (nodes that are not subdivided => flag is False) can draw a color
    color_count = sum(0 if flag else 1 for flag in subdivided_flags)
    colors = []
    for i in range(color_count):
        color = []
        for band in range(nchannels):
            if dtype == "uint8":
                color.append(decode_uint8(stream.read(1)))
            elif dtype == "uint16":
                color.append(decode_uint16(stream.read(2)))
            elif dtype == "uint32":
                color.append(decode_uint32(stream.read(4)))
            elif dtype.startswith("float"):
                color.append(decode_float(stream.read(4)))
            else:
                raise ValueError(f"Unsupported dtype: {dtype}")
        colors.append(color)

    return width, height, subdivided_flags, colors


def check_node(graph: "CompressNode", level: int, counter: float = 0) -> float:
    """Recursively checks the node and its children for estimate
    the graph's complexity.


    Args:
        graph (CompressNode): The node to check.
        level (int): The level of the node.
        counter (float, optional): The counter to increment. Defaults to 0.

    Returns:
        float: The counter.
    """
    if graph.is_subdivided:
        counter += 4.0
    else:
        return counter

    if level == 0:
        return counter
    else:
        p1 = check_node(graph.bottom_left_node, level - 1) * 1.0
        p2 = check_node(graph.bottom_right_node, level - 1) * 1.0
        p3 = check_node(graph.top_left_node, level - 1) * 1.0
        p4 = check_node(graph.top_right_node, level - 1) * 1.0
        return p1 + p2 + p3 + p4
