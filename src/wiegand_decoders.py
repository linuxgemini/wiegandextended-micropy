class GenericWiegandCardFormat:
    def __init__(self):
        self.facility_code: int = 0
        self.card_code: int = 0
        self.card_number: int = 0
        self.format_type: str = ""

def get_binary_str(wiegand_data: int, wiegand_bitcount: int) -> str:
    return "{0:0{l}b}".format(wiegand_data, l=wiegand_bitcount)

def get_hex_str(wiegand_data: int) -> str:
    return "{0:x}".format(wiegand_data)

def get_bits(wiegand_data: int, wiegand_bitcount: int):
    return [int(c) for c in get_binary_str(wiegand_data, wiegand_bitcount)]

def decode_guess(bits: list[int]) -> GenericWiegandCardFormat:
    bitlength = len(bits)
    if bitlength == 50:
        return Wiegand50ToAWID(bits)
    elif bitlength == 37:
        return Wiegand37ToHID(bits)
    elif bitlength == 35:
        return Wiegand35ToHID(bits)
    elif bitlength == 34:
        return Wiegand34ToHID(bits)
    elif bitlength == 26:
        return Wiegand26ToHID(bits)
    else:
        return GenericWiegandCardFormat()

def Wiegand50ToAWID(bits: list[int]) -> GenericWiegandCardFormat:
    AWIDcard = GenericWiegandCardFormat()
    AWIDcard.format_type = "AWID RBH50"

    # 50 bit AWID RBH50 format

    # facility code = bits 2 to 16
    for i in range(1, 17):
        AWIDcard.facility_code <<= 1
        AWIDcard.facility_code |= bits[i]

    # card code = bits 17 to 49
    for i in range(17, 49):
        AWIDcard.card_code <<= 1
        AWIDcard.card_code |= bits[i]

    return AWIDcard

def Wiegand37ToHID(bits: list[int]) -> GenericWiegandCardFormat:
    HIDcard = GenericWiegandCardFormat()
    HIDcard.format_type = "H10302 or H10304"

    # 37 bit format (H10302 or H10304)

    # H10304, FC and CC
    # FC = bits 2 to 17
    for i in range(1, 17):
        HIDcard.facility_code <<= 1
        HIDcard.facility_code |= bits[i]

    # CC = bits 18 to 36
    for i in range(17, 36):
        HIDcard.card_code <<= 1
        HIDcard.card_code |= bits[i]

    # H10302, no FC or CC, CN is used
    # bits 2 to 36
    for i in range(1, 36):
        HIDcard.card_number <<= 1
        HIDcard.card_number |= bits[i]

    if not (HIDcard.facility_code <= 65535 and HIDcard.card_code <= 524287):
        HIDcard.format_type = "H10302"

    return HIDcard

def Wiegand35ToHID(bits: list[int]) -> GenericWiegandCardFormat:
    HIDcard = GenericWiegandCardFormat()
    HIDcard.format_type = "H5XXXX (HID Corporate 1000)"

    # 35 bit HID Corporate 1000 format (H5XXXX)

    # facility code = bits 2 to 14
    for i in range(1, 14):
        HIDcard.facility_code <<= 1
        HIDcard.facility_code |= bits[i]

    # card code = bits 15 to 34
    for i in range(14, 34):
        HIDcard.card_code <<= 1
        HIDcard.card_code |= bits[i]

    return HIDcard

def Wiegand34ToHID(bits: list[int]) -> GenericWiegandCardFormat:
    HIDcard = GenericWiegandCardFormat()
    HIDcard.format_type = "H10306"

    # 34 bit format (H10306)

    # FC = bits 2 to 17
    for i in range(1, 17):
        HIDcard.facility_code <<= 1
        HIDcard.facility_code |= bits[i]

    # CC = bits 18 to 33
    for i in range(17, 33):
        HIDcard.card_code <<= 1
        HIDcard.card_code |= bits[i]

    return HIDcard

def Wiegand26ToHID(bits: list[int]) -> GenericWiegandCardFormat:
    HIDcard = GenericWiegandCardFormat()
    HIDcard.format_type = "H10301"

    # standard 26 bit format (H10301)

    # facility code = bits 2 to 9
    for i in range(1, 9):
        HIDcard.facility_code <<= 1
        HIDcard.facility_code |= bits[i]

    # card code = bits 10 to 25
    for i in range(9, 25):
        HIDcard.card_code <<= 1
        HIDcard.card_code |= bits[i]

    return HIDcard
