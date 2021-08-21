import micropython
from machine import Pin, Timer
import utime

class HIDreader:
    def __init__(self, READER_RED, READER_GRN, READER_HLD, READER_BZR, READER_TMP, hold_reader_after_read: bool = False):
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
        self.__hold_reader_after_read = hold_reader_after_read
        self.__buzzer_timer = Timer(-1)
        self.__buzzer_timer_is_active = False
        self.__buzzer_is_active = False
        self.__buzzer_current_cycle_count = 0
        self.__buzzer_cycle_limit = 8
        self.__buzzer_cycle_forever = False


    def __hold_reader(self):
        self.hold.off()
        if not self.__reader_on_hold:
            self.__reader_on_hold = True


    def __unhold_reader(self):
        self.hold.on()
        if self.__reader_on_hold:
            self.__reader_on_hold = False


    def __buzzer_on(self):
        self.buzzer.off()
        if not self.__buzzer_is_active:
            self.__buzzer_is_active = True

    def __buzzer_off(self):
        self.buzzer.on()
        if self.__buzzer_is_active:
            self.__buzzer_is_active = False


    def __toggle_buzzer(self, _):
        if self.__buzzer_is_active:
            self.__buzzer_off()
        else:
            self.__buzzer_on()

        self.__buzzer_current_cycle_count = self.__buzzer_current_cycle_count + 1

        if (
            self.__buzzer_timer_is_active and (
                self.__buzzer_current_cycle_count >= self.__buzzer_cycle_limit
                )
            ) and not self.__buzzer_cycle_forever:
            self.stop_buzzer()


    def __tamper_detect(self, newstate_pin):
        self.__tampered = False if newstate_pin.value() == 1 else True

        if self.__tampered:
            self.__hold_reader()
            self.set_led("amber")
            self.ring_buzzer_with_timer(continuous=True)
        else:
            self.__unhold_reader()
            self.set_led()
            self.stop_buzzer()

        self.tamper_callback(self.__tampered, self.__reader_on_hold)


    def get_led(self):
        r: int = self.LED["red"].value()
        g: int = self.LED["green"].value()

        f = None

        if r == 1 and g == 1:
            f = ""
        elif r == 0 and g == 1:
            f = "red"
        elif r== 1 and g == 0:
            f = "green"
        elif r == 0 and g == 0:
            f = "amber"

        return f


    def set_led(self, color: str = ""):
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


    def ring_buzzer_with_timer(self, cycle_ms: int = 125, beep_count: int = 4, continuous: bool = False):
        if beep_count < 4:
            beep_count = 4
        if cycle_ms < 125 or cycle_ms > 1250:
            cycle_ms = 125

        if not self.__buzzer_timer_is_active:
            if continuous:
                self.__buzzer_cycle_forever = True

            self.__buzzer_cycle_limit = beep_count * 2

            toggle_ms = int(cycle_ms / 2)
            self.__buzzer_timer.init(period=toggle_ms, callback=self.__toggle_buzzer)
            self.__buzzer_timer_is_active = True


    def ring_buzzer_blocking(self, cycle_ms: int = 125, beep_count: int = 4):
        if beep_count < 4:
            beep_count = 4
        if cycle_ms < 125 or cycle_ms > 1250:
            cycle_ms = 125

        cycle_count = beep_count * 2
        toggle_ms = int(cycle_ms / 2)

        for _ in range(cycle_count):
            self.__toggle_buzzer(None)
            utime.sleep_ms(toggle_ms)
        self.stop_buzzer()


    def stop_buzzer(self):
        if self.__buzzer_timer_is_active:
            self.__buzzer_timer.deinit()
            self.__buzzer_timer_is_active = False

        self.__buzzer_off()
        self.__buzzer_cycle_limit = 8
        self.__buzzer_current_cycle_count = 0
        self.__buzzer_cycle_forever = False


    def pass_light(self):
        if self.__hold_reader_after_read:
            self.__hold_reader()

        self.set_led("green")
        utime.sleep_ms(1312)

        if self.__hold_reader_after_read:
            self.__unhold_reader()

        self.set_led()


    def deny_light(self):
        if self.__hold_reader_after_read:
            self.__hold_reader()

        self.set_led("red")
        self.ring_buzzer_blocking(beep_count=10, cycle_ms=100)

        if self.__hold_reader_after_read:
            self.__unhold_reader()

        self.set_led()
