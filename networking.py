"""
Functions that let us do networking stuff
"""

import ipaddress
import random
import socket
import arpreq

from subprocess import Popen, PIPE

BASE_IP = ""
BASE_NETMASK = ""


def execute(args):
    '''
    Execute a command. Pass the args as an array if there is more than one
    '''
    retval = {'status': 255}
    try:
        proc = Popen(args, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE,
                     close_fds=True)
        retval['stdout'] = proc.stdout.read().decode("utf-8")
        retval['stderr'] = proc.stderr.read().decode("utf-8")
        retval['status'] = proc.wait()
    except Exception as E:
        print("{}: {}".format(args, E))
    return retval


def _getIp(host="1.1.1.1"):
    """Get the ip address that would be used to connect to this host
    Args:
        host (str): the host to connect to, default to an external host
    """
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.connect((host,1))
    ip = soc.getsockname()[0]
    soc.close()
    return ip

def _getSubnetMaskFromIp(ip):
    """Get the subnet mask for the given IP
    Args:
        ip (str): the ip address
    Returns:
        str: the subnet mask
    """
    res = execute("ip addr | grep -oE '{}/[^ ]+'".format(ip))  # Get three lines of output
    if res.get('status', 255) != 0:
        raise Exception("Cannot find default interface: {}".format(res.get('stderr', '')))
    mask = res['stdout'].split("/")[-1].strip()
    return "/" + mask

def getRandomIps(count=1):
    # Get all the possible hosts in the network
    myip = _getIp()
    myip = myip + _getSubnetMaskFromIp(myip)  # 192.168.0.4/24

    hosts = [ip.exploded for ip in ipaddress.IPv4Network(myip, strict=False).hosts()]
    random.shuffle(hosts) # Shuffle the list
    print("Discovering {} addresses to use...".format(count))
    addresses = set()
    # Keep looping until we run out of ip addresses or have found enough
    for ip in hosts:
        if ip not in addresses:
            if not arpreq.arpreq(ip):
                addresses.add(ip)
                print(".", end="", flush=True)
        if len(addresses) == count:
            break
    return list(addresses)