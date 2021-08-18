# main.py
from lib.wiegand import Wiegand
import lib.wiegand_decoders
import lib.helpers
from lib.hidreader import HIDreader

print("run main.py")

PIN0 = "D2"
PIN1 = "D3"

READER_RED = "D8"
READER_GRN = "D9"
READER_HLD = "D10"
READER_BZR = "D11"
READER_TMP = "D12"

try:
    # pylint: disable=used-before-assignment
    main_thread.timer.deinit() # type: ignore
except BaseException:
    pass

lib.helpers.headstart()

reader = HIDreader(READER_RED, READER_GRN, READER_HLD, READER_BZR, READER_TMP)

def print_decode_guess(guessed_decode):
    if guessed_decode.format_type != "":
        print()
        print("Wiegand data decoded:")
        print("        Format: " + guessed_decode.format_type)
        if guessed_decode.format_type == "H10302":
            print("            CN: " + str(guessed_decode.card_number))
        else:
            print("            FC: " + str(guessed_decode.facility_code))
            print("            CC: " + str(guessed_decode.card_code))
        if guessed_decode.format_type == "H10302 or H10304":
            print("            CN: " + str(guessed_decode.card_number))

def on_card(wiegand_data, wiegand_bitcount, _):
    wg_binary = lib.wiegand_decoders.get_binary_str(wiegand_data, wiegand_bitcount)
    wg_bits = lib.wiegand_decoders.get_bits(wiegand_data, wiegand_bitcount)
    wg_hex = lib.wiegand_decoders.get_hex_str(wiegand_data, wiegand_bitcount)
    guessed_decode = lib.wiegand_decoders.decode_guess(wg_bits)
    print()
    print("Wiegand data found:")
    print("    Bit Length: " + str(wiegand_bitcount))
    print("        Binary: " + wg_binary)
    print("           Hex: " + wg_hex.upper())
    print("   Reverse Hex: " + lib.helpers.hex_rev(wg_hex).upper())
    print_decode_guess(guessed_decode)
    print()
lib.helpers.sleep1sec()

main_thread = Wiegand(PIN0, PIN1, on_card)
lib.helpers.afterload()

while True:
    lib.helpers.sleep1sec()
