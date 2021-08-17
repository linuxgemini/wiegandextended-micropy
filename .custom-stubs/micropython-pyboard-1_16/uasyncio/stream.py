"""
Module: 'uasyncio.stream' on micropython-pyboard-1.16
"""
# MCU: {'ver': '1.16', 'port': 'pyboard', 'arch': 'armv7emsp', 'sysname': 'pyboard', 'release': '1.16.0', 'name': 'micropython', 'mpy': 7685, 'version': '1.16.0', 'machine': 'NUCLEO-F411RE with STM32F411xE', 'build': '', 'nodename': 'pyboard', 'platform': 'pyboard', 'family': 'micropython'}
# Stubber: 1.3.9

class Server:
    ''
    _serve = None
    def close():
        pass

    wait_closed = None

class Stream:
    ''
    aclose = None
    awrite = None
    awritestr = None
    def close():
        pass

    drain = None
    def get_extra_info():
        pass

    read = None
    readexactly = None
    readinto = None
    readline = None
    wait_closed = None
    def write():
        pass


class StreamReader:
    ''
    aclose = None
    awrite = None
    awritestr = None
    def close():
        pass

    drain = None
    def get_extra_info():
        pass

    read = None
    readexactly = None
    readinto = None
    readline = None
    wait_closed = None
    def write():
        pass


class StreamWriter:
    ''
    aclose = None
    awrite = None
    awritestr = None
    def close():
        pass

    drain = None
    def get_extra_info():
        pass

    read = None
    readexactly = None
    readinto = None
    readline = None
    wait_closed = None
    def write():
        pass

core = None
open_connection = None
start_server = None
stream_awrite = None
