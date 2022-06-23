from . import net, util, commands


# grill data response
INFO_RESPONSE = [
    ("2x", "?"), # always "UR"
    ("h", "grill_temp"),   # 2-3
    ("h", "probe1_temp"),  # 4-5
    ("h", "grill_target"), # 6-7
    ("8s", "_UC_data"), # 8-15  The "UC" command seems to send 8 bytes, and the reply always matches this
    ("h", "probe2_temp"),
    ("h", "probe2_target"),
    ("B", "curve_remain_time"),
    ("B", "_21"),
    ("B", "_22"),
    ("B", "_23"),
    ("B", "warn_code"),
    ("B", "_25"),
    ("B", "_26"),
    ("B", "_27"),
    ("h", "probe1_target"),
    ("B", "grill_state"), # 30
    ("B", "grill_mode"),
    ("B", "fire_state"),
    ("B", "fire_state_pct"),
    ("B", "_34"),
    ("B", "_35"),
]


def get(ip):
    reply = net.send_message(commands.INFO, ip)
    if len(reply) != 36:
        raise RuntimeError("mangled data", repr(reply))
    data = util.specunpack(INFO_RESPONSE, reply, byte_order="<")
    return data


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument("grill_ip")
    args = parser.parse_args()

    data = get(args.grill_ip)
    print(json.dumps(data, indent=2, sort_keys=True))


if __name__ == "__main__":
    import argparse
    import json
    import sys
    sys.exit(_main())
