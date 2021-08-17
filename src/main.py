PIN0 = "D2"
PIN1 = "D3"

READER_RED = "D8"
READER_GRN = "D9"
READER_HLD = "D10"
READER_BZR = "D11"
READER_TMP = "D12"

# main.py
print("run main.py")
from wiegand import Wiegand
import wiegand_decoders
import helpers
from hidreader import HIDreader

try:
    main_thread.timer.deinit() # type: ignore
except NameError: ""

helpers.headstart()

reader = HIDreader(READER_RED, READER_GRN, READER_HLD, READER_BZR, READER_TMP)

def on_card(wiegand_data, wiegand_bitcount, card_count):
    wg_binary = wiegand_decoders.get_binary_str(wiegand_data, wiegand_bitcount)
    wg_bits = wiegand_decoders.get_bits(wiegand_data, wiegand_bitcount)
    wg_hex = wiegand_decoders.get_hex_str(wiegand_data)
    guessed_decode = wiegand_decoders.decode_guess(wg_bits)
    print()
    print("Wiegand data found:")
    print("    Bit Length: " + str(wiegand_bitcount))
    print("        Binary: " + wg_binary)
    print("           Hex: " + wg_hex.upper())
    print("   Reverse Hex: " + helpers.hex_rev(wg_hex).upper())
    
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
    print()
helpers.sleep1sec()

main_thread = Wiegand(PIN0, PIN1, on_card)
helpers.afterload()

while True:
    helpers.sleep1sec()
    reader.set_led("orange")
    helpers.sleep1sec()
    reader.set_led("green")
    helpers.sleep1sec()
    reader.set_led("red")
    helpers.sleep1sec()
    reader.ring_buzzer()
    helpers.sleep1sec()