from machine import Pin, Timer
import utime

class HIDreader:
    def __init__(self, READER_RED, READER_GRN, READER_HLD, READER_BZR, READER_TMP):
        self.LED = {
            "red": Pin(READER_RED, Pin.OUT, value=1),
            "green": Pin(READER_GRN, Pin.OUT, value=1)
            }
        self.hold = Pin(READER_HLD, Pin.OUT, value=1)
        self.buzzer = Pin(READER_BZR, Pin.OUT, value=1)
        self.tamper = Pin(READER_TMP, Pin.IN)
        self.__tampered = False
        self.__reader_on_hold = False

    def set_led(self, color: str):
        color = color.lower()
        if color == "red":
            self.LED["red"].off()
            self.LED["green"].on()
        elif color == "green":
            self.LED["red"].on()
            self.LED["green"].off()
        elif color == "orange":
            self.LED["red"].off()
            self.LED["green"].off()
        else:
            self.LED["red"].on()
            self.LED["green"].on()

    def ring_buzzer(self, count: int = 5, play_gap_ms: int = 100):
        if count <= 0: count = 1
        if play_gap_ms <= 10: play_gap_ms = 10

        for i in range(count):
            self.buzzer.off()
            utime.sleep_ms(play_gap_ms)
            self.buzzer.on()