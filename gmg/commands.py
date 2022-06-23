INFO = b"UR001!"
ID = b"UL!"
FIRMWARE = b"UN!"
POWER_ON = b"UK001!"
POWER_OFF = b"UK004!"
CLIMATE = b"UC01234567"  # tbd.


def set_grill_temp(temp_f) -> bytes:
    if not (150 <= temp_f <= 550):
        raise ValueError("invalid temperature")
    return "UT{03d}!".format(temp_f).encode("ascii")


def set_probe_temp(temp_f, probe=1) -> bytes:
    probe_char = {
        1: "F",
        2: "f",
    }[probe]
    if not (100 <= temp_f <= 250):
        raise ValueError("invalid temperature")
    return "U{1s}{03d}!".format(probe_char, temp_f).encode("ascii")


def set_climate(payload):
    CLIMATE = b"UC"
