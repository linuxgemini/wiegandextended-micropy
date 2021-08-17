"""
Module: 'uasyncio.event' on micropython-pyboard-1.16
"""
# MCU: {'ver': '1.16', 'port': 'pyboard', 'arch': 'armv7emsp', 'sysname': 'pyboard', 'release': '1.16.0', 'name': 'micropython', 'mpy': 7685, 'version': '1.16.0', 'machine': 'NUCLEO-F411RE with STM32F411xE', 'build': '', 'nodename': 'pyboard', 'platform': 'pyboard', 'family': 'micropython'}
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
