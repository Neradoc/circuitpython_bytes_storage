# SPDX-FileCopyrightText: Copyright (c) 2021 Neradoc
# SPDX-License-Identifier: MIT
from bytes_storage import *

data = {"name": "nvm_helper", "num": 92, "float": 3.14}

storage = ByteArrayStorage(1024)
storage.save(data)
print(storage.read())

storage = SleepMemoryStorage()
storage.save(data)
print(storage.read())

storage = NVMStorage()
storage.save(data)
print(storage.read())
