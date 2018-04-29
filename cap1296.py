try:
    from micropython import const
except ModuleNotFoundError:
    const = lambda c: c

# important registers
MAIN_CONTROL = const(0x00)
SENSOR_INPUT_STATUS = const(0x03)
SENSOR_INPUT_ENABLE = const(0x21)
INTERRUPT_ENABLE = const(0x27)
SIGNAL_GUARD_ENABLE = const(0x29)
MULTIPLE_TOUCH_CONFIG = const(0x2A)

def _keys_to_byte(keys, default=b'\x00'):
    return bytes([sum(map(lambda b: 1<<b, keys))]) if keys else default


class CAP1296:
    def __init__(self, i2c_handler):
        self.i2c = i2c_handler
        self._addr = 0x28
    
        self.write = lambda r, b: self.i2c.writeto_mem(self._addr, r, b)
        self.read = lambda r, n: self.i2c.readfrom_mem(self._addr, r, n)

    @property
    def address(self):
        return self._addr

    def enable_interrupt(self, keys):
        self.write(INTERRUPT_ENABLE, _keys_to_byte(keys, default=b'\x3f'))

    def enable_keys(self, keys):
        self.write(SENSOR_INPUT_ENABLE, _keys_to_byte(keys, default=b'\x3f'))   

    def enable_signal_guard(self, keys):
        assert 2 not in keys, 'cannot set key 2 (CS3), it is the SG channel'
        self.write(SIGNAL_GUARD_ENABLE, _keys_to_byte(keys))

    def read_keys(self):
        status = self.read(SENSOR_INPUT_STATUS, 1)
        self.write(MAIN_CONTROL, b'\x00')  # enables next touch reading
        return int.from_bytes(status, 'little')
