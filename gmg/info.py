from . import net, util, commands


# grill data response
INFO_RESPONSE = [
    ("2x", "?"), # "UR"
    ("h", "grill_temp"), # 2-3
    ("h", "probe1_temp"), # 4-5
    ("h", "grill_target"), # 6-7
    ("x", "?"), # 8
    ("x", "?"), # 9
    ("x", "?"), # 10
    ("x", "?"), # 11
    ("x", "?"), # 12
    ("x", "?"), # 13
    ("x", "?"), # 14
    ("x", "?"), # 15
    ("h", "probe2_temp"),
    ("x", "?"),
    ("x", "?"),
    ("b", "curve_remain_time"),
    ("x", "?"),
    ("x", "?"),
    ("x", "?"),
    ("b", "warn_code"),
    ("x", "?"),
    ("x", "?"),
    ("x", "?"),
    ("h", "probe1_target"),
    ("b", "grill_state"), # 30
    ("b", "grill_mode"),
    ("b", "fire_state"),
    ("b", "fire_state_pct"),
    ("x", "?"),
    ("x", "?"),
]


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument("grill_ip")
    args = parser.parse_args()

    reply = net.send_message(commands.INFO, args.grill_ip)
    info = util.specunpack(INFO_RESPONSE, reply, byte_order="<")

    print(json.dumps(info, indent=2, sort_keys=True))


if __name__ == "__main__":
    import argparse
    import json
    import sys
    sys.exit(_main())
