import pytest

from . import util

@pytest.mark.parametrize(
    "byte_order, output",
    [("", 0x0302), (">", 0x0302), ("<", 0x0203)],
)
def test_byte_order(byte_order, output):
    spec = [("h", "short")]
    buf = b"\x02\x03"
    output = util.specunpack(spec, buf, byte_order=byte_order)
    assert output["short"] == 0x0302


def test_name_conflict():
    spec = [
        ("h", "short"),
        ("h", "short"),
    ]
    buf = b"\x00\x01\x02\x03"
    with pytest.raises(ValueError):
        _output = util.specunpack(spec, buf)


def test_ignore_pads():
    spec = [
        ("x", "char"),
        ("4x", "char"),
        ("c", "char"),
        ("10x", "char"),
    ]
    buf = b"\x13" * 13
    output = util.specunpack(spec, buf)
    assert output["char"] == 0x13
