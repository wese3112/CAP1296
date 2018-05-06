# CAP1296
Micropython module for Microchip CAP1296 I2C touch controller. You should have a working knowledge of how the CAP1296 works, please check out its datasheet.

## Examples
I'm using a NodeMCU with Micropython (FW 1.9.3). A minimal working example starts with this setup:

    # SETUP
    import machine
    import cap1296

    # NodeMCU I2C interface
    i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4), freq=400000)
    tc = cap1296.CAP1296(i2c)  # touch controller

Then we can get the status of the CAP's sensor input register using the *read_keys* function like this.

    # No multitouch, print keys status as a byte
    keys_now, keys_before = 0, 0
    while True:
        keys_now, keys_before = tc.read_keys(), keys_now

        if keys_now != keys_before:  # keys state changed
            print(keys_now)

This prints a byte of the keys status each time the input changes (note that the output might be different than below if the byte is printable).

    b'\x00'  # no key pressed
    b'\x01'  # key 0 pressed
    b'\x00'
    b'\x02'  # key 1 pressed
    b'\x00'
    b'\x04'  # key 2 pressed
    ...

If you want multitouch and a list of all currently pressed keys, try this:

    # Multitouch enabled, print list of pressed keys
    tc.enable_multitouch(True)

    # same as in the example above
    keys_now, keys_before = 0, 0
    while True:
        keys_now, keys_before = tc.read_keys(as_list=True), keys_now

        if keys_now != keys_before:  # user input occured
            print(keys_now)

This gives you:

    []  # no key pressed
    [0]  # key 0 pressed
    [0, 1]  # key 0 and 1 pressed
    []  # no key pressed
    [1]  # key 1 pressed
    [0, 1, 2, 3, 4]  # keys 0 to 4 pressed

## Todo
+ the *enable_signal_guard* function is untested yet