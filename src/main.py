# main.py
import lib.helpers
import lib.wiegand_decoders
import lib.screen
from lib.wiegand import Wiegand
from lib.hidreader import HIDreader

print("run main.py")

__PIN0 = 7 # Pin 10, GP7
__PIN1 = 8 # Pin 11, GP8

__READER_RED = 2 # Pin 4, GP2
__READER_GRN = 3 # Pin 5, GP3
__READER_HLD = 4 # Pin 6, GP4
__READER_BZR = 5 # Pin 7, GP5
__READER_TMP = 6 # Pin 9, GP6

__SCREEN_SDA = 20 # Pin 26, GP20, I2C0 SDA
__SCREEN_SCL = 21 # Pin 27, GP21, I2C0 SCL

__allowed_cards = [
    lib.wiegand_decoders.GenericWiegandCardFormat(54, 64004, 0, "H10301"), # HID SEOS
    lib.wiegand_decoders.GenericWiegandCardFormat(95, 10491, 0, "H10301"), # HID Prox
    0x02840069, # STMicro M24SR64-Y UID 32bit LSB
    0x69008402, # STMicro M24SR64-Y UID 32bit MSB
    ]


try:
    # pylint: disable=used-before-assignment
    __wiegand_sync_thread.timer.deinit() # type: ignore
except BaseException:
    pass


lib.helpers.headstart()


__reader = HIDreader(__READER_RED, __READER_GRN, __READER_HLD, __READER_BZR, __READER_TMP)
__screen = lib.screen.init_screen(__SCREEN_SDA, __SCREEN_SCL, True, True)

def __card_check(wiegand_data: int, guessed_decode: lib.wiegand_decoders.GenericWiegandCardFormat):
    if len(__allowed_cards) == 0:
        return True

    for card in __allowed_cards:
        if isinstance(card, int):
            if card == wiegand_data:
                return True
        elif isinstance(card, lib.wiegand_decoders.GenericWiegandCardFormat):
            c1 = (card.facility_code == guessed_decode.facility_code)
            c2 = (card.card_code == guessed_decode.card_code)
            c3 = (card.card_number == guessed_decode.card_number)
            if c1 and c2 and c3:
                return True

    return False


def __print_decode_guess(guessed_decode):
    if guessed_decode.format_type != "":
        print()
        print("Wiegand data decoded:")
        print("        Format: " + guessed_decode.format_type)
        if guessed_decode.format_type == "H10302":
            print("            CN: " + str(guessed_decode.card_number))
            __screen.putstr(str(guessed_decode.card_number))
        else:
            print("            FC: " + str(guessed_decode.facility_code))
            print("            CC: " + str(guessed_decode.card_code))
            __screen.putstr(str(guessed_decode.facility_code) + ", " + str(guessed_decode.card_code))
        if guessed_decode.format_type == "H10302 or H10304":
            print("            CN: " + str(guessed_decode.card_number))


def __on_card(wiegand_data, wiegand_bitcount, _):
    wg_binary = lib.wiegand_decoders.get_binary_str(wiegand_data, wiegand_bitcount)
    wg_bits = lib.wiegand_decoders.get_bits(wiegand_data, wiegand_bitcount)
    wg_hex = lib.wiegand_decoders.get_hex_str(wiegand_data, wiegand_bitcount)
    guessed_decode = lib.wiegand_decoders.decode_guess(wg_bits)
    print()
    __screen.clear()
    __screen.putstr("Hex: " + wg_hex.upper() + "\n")
    print("Wiegand data found:")
    print("    Bit Length: " + str(wiegand_bitcount))
    print("        Binary: " + wg_binary)
    print("           Hex: " + wg_hex.upper())
    print("   Reverse Hex: " + lib.helpers.hex_rev(wg_hex).upper())
    __print_decode_guess(guessed_decode)
    print()
    pass_chk = __card_check(wiegand_data, guessed_decode)
    if pass_chk:
        __reader.pass_light()
    else:
        __reader.deny_light()
    __rs_scr()
lib.helpers.sleep()


def __rs_scr():
    __screen.clear()
    __screen.backlight_on()
    __screen.putstr("Ready to read.\n")
    __screen.blink_cursor_off()
    __screen.hide_cursor()

__wiegand_sync_thread = Wiegand(__PIN0, __PIN1, __on_card)
lib.helpers.afterload()

__rs_scr()
