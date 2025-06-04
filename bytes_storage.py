# SPDX-FileCopyrightText: Copyright (c) 2021 Neradoc
# SPDX-License-Identifier: MIT
import microcontroller
import msgpack
from io import BytesIO

try:
    import alarm
except ImportError:
    pass

class ByteStorage:
    def __init__(self, storage_facility: bytearray, offset:int = 0):
        self.storage = storage_facility
        self.offset = offset

    def save(self, data):
        packed_data_io = BytesIO()
        msgpack.pack(data, packed_data_io)
        length = packed_data_io.tell()

        if length + 8 + self.offset > len(self.storage):
            raise ValueError("Data can't fit into storage facility")

        self.storage[self.offset:self.offset+8] = length.to_bytes(8, "big")
        self.storage[self.offset+8:self.offset+8+length] = packed_data_io.getvalue()

    def load(self):
        length_s = self.storage[self.offset:self.offset+8]
        length = int.from_bytes(length_s, "big")

        if length > len(self.storage) - 8:
            return None

        data_s = self.storage[self.offset+8:self.offset+8+length]
        try:
            data = msgpack.unpack(BytesIO(data_s))
            return data
        except ValueError:
            return None

    def __len__(self):
        return len(self.storage)

class ByteArrayStorage(ByteStorage):
    def __init__(self, size:int):
        super().__init__(bytearray(size))

class SleepMemoryStorage(ByteStorage):
    def __init__(self, offset:int = 0):
        super().__init__(alarm.sleep_memory, offset)

class NVMStorage(ByteStorage):
    def __init__(self, offset:int = 0):
        super().__init__(microcontroller.nvm, offset)

class FileStorage():
    def __init__(self, file):
        self.file = file

    def save(self, data):
        packed_data_io = BytesIO()
        msgpack.pack(data, packed_data_io)
        length = packed_data_io.tell()

        with open(self.file, "wb") as fp:
            fp.write(packed_data_io.getvalue())

    def load(self):
        try:
            with open(self.file, "rb") as fp:
                data_s = fp.read()
        except OSError:
            return None

        try:
            data = msgpack.unpack(BytesIO(data_s))
            return data
        except ValueError:
            return None

    def __len__(self):
        try:
            stat = os.stat(self.file)
            return stat[6]
        except OSError:
            return 0

def _test():
    import alarm
    import microcontroller
    data = {"name": "nvm_helper", "num": 92, "float": 3.14}
    storage = ByteArrayStorage(bytearray(1024))
    storage.save(data)
    print(storage.load())
