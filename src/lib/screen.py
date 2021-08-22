from machine import SoftI2C
from lcd.machine_i2c_lcd import I2cLcd

def init_screen(pin_sda, pin_scl):
    i2c = SoftI2C(sda=pin_sda, scl=pin_scl)
    addr = i2c.scan()[0]

    return I2cLcd(i2c, addr, 2, 16)
