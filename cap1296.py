try:
    from micropython import const
except ImportError:
    def const(var):
        return var

CAP1296_I2C_ADDRESS = const(0x28)

# important registers
MAIN_CONTROL = const(0x00)
SENSOR_INPUT_STATUS = const(0x03)
SENSOR_INPUT_ENABLE = const(0x21)
INTERRUPT_ENABLE = const(0x27)
SIGNAL_GUARD_ENABLE = const(0x29)
MULTIPLE_TOUCH_CONFIG = const(0x2A)


def _keys_to_byte(keys: list, default=b'\x00') -> bytes:
    """Return a byte in which the bits X are 1 for each X in the list keys."""
    return bytes([sum(map(lambda b: 1 << b, keys))]) if keys else default


def _byte_to_keys(keys_as_byte: bytes, num_keys=6) -> list:
    """Return a list of key (bit) numbers for each 1 in keys_as_byte."""
    keys_as_int = int.from_bytes(keys_as_byte, byteorder='little')
    return [
        key
        for key in range(num_keys)
        if keys_as_int & (1 << key)
    ]


class CAP1296:
    def __init__(self, i2c_handler):
        self.i2c = i2c_handler
        self._addr = CAP1296_I2C_ADDRESS
    
        self.write = lambda r, b: self.i2c.writeto_mem(self._addr, r, b)
        self.read = lambda r, n: self.i2c.readfrom_mem(self._addr, r, n)

    def enable_interrupt(self, keys: list):
        self.write(INTERRUPT_ENABLE, _keys_to_byte(keys, default=b'\x3f'))

    def enable_keys(self, keys: list):
        self.write(SENSOR_INPUT_ENABLE, _keys_to_byte(keys, default=b'\x3f'))   

    def enable_signal_guard(self, keys: list):
        assert 2 not in keys, 'cannot set key 2 (CS3), it is the SG channel'
        self.write(SIGNAL_GUARD_ENABLE, _keys_to_byte(keys))

    def read_keys(self, as_byte=True):
        status = self.read(SENSOR_INPUT_STATUS, 1)
        self.write(MAIN_CONTROL, b'\x00')  # enables next touch reading

        if as_byte:
            return int.from_bytes(status, byteorder='little')
        else:
            return _byte_to_keys(status, num_keys=5)
