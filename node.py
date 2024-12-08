# node.py
from utils import (
    BLOCK_SIZE, MAX_KEYS, MAX_CHILDREN,
    to_big_endian_8, from_big_endian_8
)

class Node:
    def __init__(self, block_id=0, parent_id=0, num_keys=0):
        self.block_id = block_id
        self.parent_id = parent_id
        self.num_keys = num_keys
        self.keys = [0]*(MAX_KEYS)
        self.values = [0]*(MAX_KEYS)
        self.children = [0]*(MAX_CHILDREN)

    @classmethod
    def read_from_file(cls, f, block_id: int):
        f.seek(block_id*BLOCK_SIZE)
        data = f.read(BLOCK_SIZE)
        if len(data) < BLOCK_SIZE:
            raise ValueError("Block read is too short.")

        n = cls()
        pos = 0

        # block_id
        n.block_id = from_big_endian_8(data[pos:pos+8])
        pos += 8
        # parent_id
        n.parent_id = from_big_endian_8(data[pos:pos+8])
        pos += 8
        # num_keys
        n.num_keys = from_big_endian_8(data[pos:pos+8])
        pos += 8

        # keys
        for i in range(MAX_KEYS):
            n.keys[i] = from_big_endian_8(data[pos:pos+8])
            pos += 8

        # values
        for i in range(MAX_KEYS):
            n.values[i] = from_big_endian_8(data[pos:pos+8])
            pos += 8

        # children
        for i in range(MAX_CHILDREN):
            n.children[i] = from_big_endian_8(data[pos:pos+8])
            pos += 8

        return n

    def write_to_file(self, f):
        f.seek(self.block_id*BLOCK_SIZE)
        out = b''
        out += to_big_endian_8(self.block_id)
        out += to_big_endian_8(self.parent_id)
        out += to_big_endian_8(self.num_keys)
        for i in range(MAX_KEYS):
            out += to_big_endian_8(self.keys[i])
        for i in range(MAX_KEYS):
            out += to_big_endian_8(self.values[i])
        for i in range(MAX_CHILDREN):
            out += to_big_endian_8(self.children[i])

        if len(out) > BLOCK_SIZE:
            raise ValueError("Node data exceeds block size.")
        out = out + b'\x00'*(BLOCK_SIZE - len(out))
        f.write(out)