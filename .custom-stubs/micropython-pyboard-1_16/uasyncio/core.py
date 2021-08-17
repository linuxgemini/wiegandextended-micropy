"""
Module: 'uasyncio.core' on micropython-pyboard-1.16
"""
# MCU: {'ver': '1.16', 'port': 'pyboard', 'arch': 'armv7emsp', 'sysname': 'pyboard', 'release': '1.16.0', 'name': 'micropython', 'mpy': 7685, 'version': '1.16.0', 'machine': 'NUCLEO-F411RE with STM32F411xE', 'build': '', 'nodename': 'pyboard', 'platform': 'pyboard', 'family': 'micropython'}
# Stubber: 1.3.9

class CancelledError:
    ''

class IOQueue:
    ''
    def _dequeue():
        pass

    def _enqueue():
        pass

    def queue_read():
        pass

    def queue_write():
        pass

    def remove():
        pass

    def wait_io_event():
        pass


class Loop:
    ''
    _exc_handler = None
    def call_exception_handler():
        pass

    def close():
        pass

    def create_task():
        pass

    def default_exception_handler():
        pass

    def get_exception_handler():
        pass

    def run_forever():
        pass

    def run_until_complete():
        pass

    def set_exception_handler():
        pass

    def stop():
        pass


class SingletonGenerator:
    ''

class Task:
    ''

class TaskQueue:
    ''
    def peek():
        pass

    def pop_head():
        pass

    def push_head():
        pass

    def push_sorted():
        pass

    def remove():
        pass


class TimeoutError:
    ''
_exc_context = None
_io_queue = None
def _promote_to_task():
    pass

_stop_task = None
_stopper = None
_task_queue = None
def create_task():
    pass

def current_task():
    pass

def get_event_loop():
    pass

def new_event_loop():
    pass

def run():
    pass

def run_until_complete():
    pass

select = None
def sleep():
    pass

def sleep_ms():
    pass

sys = None
def ticks():
    pass

def ticks_add():
    pass

def ticks_diff():
    pass

