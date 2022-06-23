import requests

import gmg.info
import gmg.net
import gmg.util


def write_influx(addr, data, db="kelvin"):
    url = addr + "/write"
    params = {"db": db}
    headers = {'Content-Type': 'application/octet-stream'}
    response = requests.post(url, params=params, data=data, headers=headers)
    return response


# grills = gmg.net.find_grills("192.168.42.0/24")
# grill = grills[0]
# grill

# get_info(grill)
