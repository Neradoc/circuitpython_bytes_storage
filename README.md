Small helper to save structured data into a bytearray like NVM or alarm memory.
Simply swap the class for the type of storage you want to use.

`ByteStorage`: An object compatible with the bytearray interface can be used, like some external EEPROM libraries. For example the [24LC32 I2C EEPROM](https://github.com/adafruit/Adafruit_CircuitPython_24LC32).

`NVMStorage`: NVM (non volatile memory) is implemented with `microcontroller.nvm` and stored in flash. It is not erased when the board is reset and can be used to store settings. Be careful not to get your code in a loop that writes quickly multiple times, as flash memory is rated for a limited number of erase/write cycles, typically in the 150 000 for the chips used with Circuitpython boards, which is a lot for normal use.

`SleepMemoryStorage`: sleep memory, in the `alarm` module, can be used to keep temporary data in RAM during deep sleep or soft reloads and possibly when resetting with `microcontroller.reset()`. It can be used to communicate data between different scripts when using `supervisor.set_next_code_file` for example, or between code.py and boot.py.

`ByteArrayStorage`: simply uses a generic bytearray of given size. This is not very useful except for testing purposes.

`FileStorage`: use a file as storage for your data. This provides a common interface with the other classes to make it easier to swap to using a file from another implementation or the other way around.

Each class supports the following methods:
- `store.load()`: returns the currently stored data, or None.
- `store.save(data)`: saves the given python structure to the storage.

### Usage

```py
from bytes_storage import *
# Example data
data = {"name": "nvm_helper", "num": 92, "float": 3.14}

store = NVMStorage()
store.save(data)
print(store.load())
```

```py
store = ByteArrayStorage(1024)
store.save(data)
print(store.load())
```

```py
store = SleepMemoryStorage()
store.save(data)
print(store.load())
```
