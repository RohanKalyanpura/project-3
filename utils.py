# utils.py
import os

MAGIC_NUMBER = b'4337PRJ3'
BLOCK_SIZE = 512
T = 10  # minimal degree
MAX_KEYS = 2*T - 1  # 19
MAX_CHILDREN = MAX_KEYS + 1  # 20

def file_exists(filename):
    return os.path.exists(filename)

def to_big_endian_8(n: int) -> bytes:
    return n.to_bytes(8, 'big', signed=False)

def from_big_endian_8(b: bytes) -> int:
    return int.from_bytes(b, 'big', signed=False)

def pad_block(data: bytes) -> bytes:
    if len(data) > BLOCK_SIZE:
        raise ValueError("Data exceeds block size.")
    return data + b'\x00'*(BLOCK_SIZE - len(data))