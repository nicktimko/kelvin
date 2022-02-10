INFO = b"UR001!"
ID = b"UL!"
FIRMWARE = b"UN!"
POWER_ON = b"UK001!"
POWER_OFF = b"UK004!"


def set_grill_temp(temp_f) -> bytes:
    if not (150 <= temp_f <= 600):
        raise ValueError("invalid temperature")
    return "UT{03d}!".format(temp_f).encode("ascii")


def set_probe_temp(temp_f) -> bytes:
    if not (32 <= temp_f <= 300):
        raise ValueError("invalid temperature")
    return "UF{03d}!".format(temp_f).encode("ascii")
