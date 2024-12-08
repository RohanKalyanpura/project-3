# indexfile.py
from utils import (
    file_exists, MAGIC_NUMBER, BLOCK_SIZE,
    to_big_endian_8, from_big_endian_8
)

class IndexFile:
    def __init__(self, filename):
        self.filename = filename
        self.f = None
        self.root_block_id = 0
        self.next_block_id = 1  # after header
        self.is_open = False

    def create_new(self, overwrite=True):
        if file_exists(self.filename) and not overwrite:
            return False
        self.f = open(self.filename, "wb+")
        header = MAGIC_NUMBER
        header += to_big_endian_8(self.root_block_id)
        header += to_big_endian_8(self.next_block_id)
        header += b'\x00'*(BLOCK_SIZE - len(header))
        self.f.write(header)
        self.f.flush()
        self.is_open = True
        return True

    def open_existing(self):
        if not file_exists(self.filename):
            return False
        self.f = open(self.filename, "rb+")
        header = self.f.read(BLOCK_SIZE)
        if header[:8] != MAGIC_NUMBER:
            return False
        self.root_block_id = from_big_endian_8(header[8:16])
        self.next_block_id = from_big_endian_8(header[16:24])
        self.is_open = True
        return True

    def update_header(self):
        self.f.seek(0)
        header = MAGIC_NUMBER
        header += to_big_endian_8(self.root_block_id)
        header += to_big_endian_8(self.next_block_id)
        header += b'\x00'*(BLOCK_SIZE - len(header))
        self.f.write(header)
        self.f.flush()

    def close(self):
        if self.is_open:
            self.update_header()
            self.f.close()
            self.is_open = False

    def allocate_new_block(self):
        bid = self.next_block_id
        self.next_block_id += 1
        self.update_header()
        return bid