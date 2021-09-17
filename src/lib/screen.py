from machine import SoftI2C, I2C, Pin
from lcd.machine_i2c_lcd import I2cLcd

def init_screen(pin_sda, pin_scl, conv_to_pin_obj=False, use_hw_i2c=False, hw_i2c_slot=0):
    if conv_to_pin_obj:
        pin_sda = Pin(pin_sda)
        pin_scl = Pin(pin_scl)

    if use_hw_i2c:
        i2c = I2C(hw_i2c_slot, sda=pin_sda, scl=pin_scl)
    else:
        i2c = SoftI2C(sda=pin_sda, scl=pin_scl)

    addr = i2c.scan()[0]

    return I2cLcd(i2c, addr, 2, 16)
