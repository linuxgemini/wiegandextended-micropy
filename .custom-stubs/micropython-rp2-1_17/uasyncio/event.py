"""
Module: 'uasyncio.event' on micropython-rp2-1.17
"""
# MCU: {'family': 'micropython', 'sysname': 'rp2', 'version': '1.17.0', 'build': '', 'mpy': 5637, 'port': 'rp2', 'platform': 'rp2', 'name': 'micropython', 'arch': 'armv7m', 'machine': 'Raspberry Pi Pico with RP2040', 'nodename': 'rp2', 'ver': '1.17', 'release': '1.17.0'}
# Stubber: 1.3.9

class Event:
    ''
    def clear():
        pass

    def is_set():
        pass

    def set():
        pass

    wait = None

class ThreadSafeFlag:
    ''
    def ioctl():
        pass

    def set():
        pass

    wait = None
core = None
uio = None
