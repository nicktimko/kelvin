"""Networking. Finding the grill and such."""

import base64
import ipaddress
import socket
import subprocess
import typing


class MAC:
    """MAC or MAC Prefix"""
    def __init__(self, address):
        self.raw = base64.b16decode(address.replace(":", ""), casefold=True)

    def __repr__(self):
        return f"{self.__class__.__name__}(address='{self}')"

    def __str__(self):
        return ":".join(hex(b)[2:] for b in self.raw)

    def __contains__(self, other):
        """Does this MAC prefix contain the provided MAC?"""
        return other.raw.startswith(self.raw)


class AddressPair(typing.NamedTuple):
    mac: MAC
    ip: str


KNOWN_PREFIX = MAC("7c:a7:b0")


def local_macs(cidr: ipaddress.IPv4Address) -> typing.List[AddressPair]:
    """
    Given a local IP CIDR range, return pairs of MAC Address and IP addresses.

    Probably only works on Linux, and needs nmap and such. Also expects Ethernet.
    """
    network = ipaddress.IPv4Network(cidr)
    # attempt connection to everything to populate ARP
    subprocess.check_output(["nmap", "-sP", str(network)])

    # dump ARP table
    neighbors = subprocess.check_output(["ip", "neighbor", "show"], universal_newlines=True)

    # and parse output from `ip neigh`
    arp_pairs = []
    for line in neighbors.splitlines():
        ip, _dev, interface, result = line.split(" ", 3)
        result = result.strip()
        if "lladdr" not in result:
            # FAILED, INCOMPLETE, etc.
            continue
        # REACHABLE, STALE, DELAY, etc.
        _lladdr, mac, status = result.split()
        arp_pairs.append(AddressPair(MAC(mac), ip))

    return arp_pairs


def find_grills(cidr):
    pairs = local_macs(cidr)
    ips = [p.ip for p in pairs if p.mac in KNOWN_PREFIX]
    return ips


def send_message(message: bytes, ip: str, *, port: int = 8080):
    address = (ip, port)
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as sock:
        sock.connect(address)
        sock.send(message)
        return sock.recv(128)


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ip_range")

    args = parser.parse_args()

    grills = find_grills(args.ip_range)
    if not grills:
        print("No grills found", file=sys.stderr)
        return 1
    if len(grills) > 1:
        print(f"Multiple possible grills found: {grills}", file=sys.stderr)
        return 2
    grill = grills[0]
    print(grill)


if __name__ == "__main__":
    import argparse
    import sys
    sys.exit(_main())
