import micropython
from machine import Pin, Timer

class HIDreader:
    def __init__(self, READER_RED, READER_GRN, READER_HLD, READER_BZR, READER_TMP):
        micropython.alloc_emergency_exception_buf(100)
        self.LED = {
            "red": Pin(READER_RED, Pin.OUT, value=1),
            "green": Pin(READER_GRN, Pin.OUT, value=1)
            }
        self.hold = Pin(READER_HLD, Pin.OUT, value=1)
        self.buzzer = Pin(READER_BZR, Pin.OUT, value=1)
        self.tamper = Pin(READER_TMP, Pin.IN)
        self.tamper.irq(trigger=(Pin.IRQ_FALLING | Pin.IRQ_RISING), handler=self.__tamper_detect)
        self.tamper_callback = lambda t, h: [t, h]
        self.__tampered = False
        self.__reader_on_hold = False
        self.__buzzer_timer = Timer(-1)
        self.__buzzer_timer_is_active = False
        self.__buzzer_is_active = False
        self.__buzzer_current_cycle_count = 0
        self.__buzzer_cycle_limit = 8
        self.__buzzer_cycle_forever = False

    def __toggle_buzzer(self, _):
        self.__buzzer_is_active = False if self.buzzer.value() == 1 else True

        if self.__buzzer_is_active:
            self.buzzer.on()
            self.__buzzer_is_active = False
        else:
            self.buzzer.off()
            self.__buzzer_is_active = True

        self.__buzzer_current_cycle_count = self.__buzzer_current_cycle_count + 1

        if (self.__buzzer_current_cycle_count >= self.__buzzer_cycle_limit) and not self.__buzzer_cycle_forever:
            self.stop_buzzer()

    def __tamper_detect(self, newstate_pin):
        self.__tampered = False if newstate_pin.value() == 1 else True

        if self.__tampered:
            self.hold.off()
            self.__reader_on_hold = True
            self.set_led("amber")
            self.ring_buzzer(continuous=True)
        else:
            self.hold.on()
            self.__reader_on_hold = False
            self.set_led("")
            self.stop_buzzer()

        self.tamper_callback(self.__tampered, self.__reader_on_hold)

    def set_led(self, color: str):
        color = color.lower()
        if color == "red":
            self.LED["red"].off()
            self.LED["green"].on()
        elif color == "green":
            self.LED["red"].on()
            self.LED["green"].off()
        elif color == "amber":
            self.LED["red"].off()
            self.LED["green"].off()
        else:
            self.LED["red"].on()
            self.LED["green"].on()

    def ring_buzzer(self, cycle_ms: int = 125, beep_count: int = 4, continuous: bool = False):
        if not self.__buzzer_timer_is_active:
            if beep_count < 4:
                beep_count = 4
            if cycle_ms < 125 or cycle_ms > 1250:
                cycle_ms = 125

            if continuous:
                self.__buzzer_cycle_forever = True

            self.__buzzer_cycle_limit = beep_count * 2

            toggle_ms = int(cycle_ms / 2)
            self.__buzzer_timer.init(period=toggle_ms, callback=self.__toggle_buzzer)
            self.__buzzer_timer_is_active = True

    def stop_buzzer(self):
        if self.__buzzer_timer_is_active:
            self.__buzzer_timer.deinit()
            self.__buzzer_timer_is_active = False

        self.buzzer.on()
        self.__buzzer_is_active = False
        self.__buzzer_cycle_limit = 8
        self.__buzzer_current_cycle_count = 0
        self.__buzzer_cycle_forever = False
