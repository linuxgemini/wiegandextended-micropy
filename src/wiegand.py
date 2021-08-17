"""
wiegand.py - read card IDs from a wiegand card reader

(C) 2017 Paul Jimenez - released under LGPLv3+
(C) 2021 linuxgemini
"""
from machine import Pin, Timer
import utime
import micropython

class Wiegand:
    def __init__(self, pin0, pin1, callback):
        """
        pin0 - the GPIO that goes high when a zero is sent by the reader
        pin1 - the GPIO that goes high when a one is sent by the reader
        callback - the function called (with two args: card ID and cardcount)
                   when a card is detected.  Note that micropython interrupt
                   implementation limitations apply to the callback!
        """
        micropython.alloc_emergency_exception_buf(100)
        self.pin0 = Pin(pin0, Pin.IN)
        self.pin1 = Pin(pin1, Pin.IN)
        self.callback = callback
        self.last_card = None
        self.last_card_bitcount = 0
        self.next_card = 0
        self._bits = 0
        self.pin0.irq(trigger=Pin.IRQ_FALLING, handler=self._on_pin0)
        self.pin1.irq(trigger=Pin.IRQ_FALLING, handler=self._on_pin1)
        self.last_bit_read = None
        self.timer = Timer(-1)
        self.timer.init(period=50, mode=Timer.PERIODIC, callback=self._cardcheck)
        self.cards_read = 0

    def _on_pin0(self, newstate):
        self._on_pin(0, newstate)

    def _on_pin1(self, newstate):
        self._on_pin(1, newstate)

    def _on_pin(self, is_one, _):
        now = utime.ticks_ms()
        if self.last_bit_read is not None and now - self.last_bit_read < 2:
            # too fast
            return

        self.last_bit_read = now
        self.next_card <<= 1
        if is_one:
            self.next_card |= 1
        self._bits += 1

    def _cardcheck(self, _):
        if self.last_bit_read is None:
            return
        now = utime.ticks_ms()
        if now - self.last_bit_read > 50:
            # too slow - new start!
            self.last_bit_read = None
            self.last_card = self.next_card
            self.last_card_bitcount = self._bits
            self.next_card = 0
            self._bits = 0
            self.cards_read += 1
            self.callback(self.last_card, self.last_card_bitcount, self.cards_read)
