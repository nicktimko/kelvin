import struct


def specunpack(spec, buf, byte_order=""):
    """
    Given a 'spec' for a structure which is a sequence of tuple pairs, each
    consisting of a struct format character and a 'name'. On unpacking 'buf',
    the names are used in the returned dictionary.

    Pad characters ('x') are ignored; the name in those pairs is irrelevant.
    """
    format_ = [byte_order]
    names = set()
    for part, name in spec:
        format_.append(part)
        if "x" in part:
            continue
        if name in names:
            raise ValueError(f"duplicate names: {name}")
        names.add(name)
    unpacked = struct.unpack("".join(format_), buf)
    output = {}
    for name, data in zip((name for part, name in spec if "x" not in part), unpacked):
        output[name] = data
    return output
