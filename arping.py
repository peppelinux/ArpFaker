#!/usr/bin/env python3

# suppress "WARNING: No route found for IPv6 destination :: (no default route?)"
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

import sys
import argparse
from scapy.all import *

def get_mac(ip, interface):
    result = ''
    arp_request = Ether(src=get_if_hwaddr(interface),dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip)
    ans, unans = srp(arp_request, timeout=2, iface=interface, verbose=False)
    if ans:
        first_response = ans[0]
        req, res = first_response
        result = res.getlayer(Ether).src

    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ip', type=str,
                        help='IP of the host you want to arp ping')
    parser.add_argument('-i', '--interface', type=str, dest='interface', default='wlan0',
                        help='Network interface to use')
    args = parser.parse_args()
    
    fetched_mac = get_mac(args.ip, args.interface)
    if fetched_mac: print("{} = {}".format(args.ip, fetched_mac ))
