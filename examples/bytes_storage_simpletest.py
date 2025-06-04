# SPDX-FileCopyrightText: Copyright (c) 2021 Neradoc
# SPDX-License-Identifier: MIT
from bytes_storage import *

data = {"name": "nvm_helper", "num": 92, "float": 3.14}

store = ByteArrayStorage(1024)
store.save(data)
print(store.load())

store = SleepMemoryStorage()
store.save(data)
print(store.load())

store = NVMStorage()
store.save(data)
print(store.load())
