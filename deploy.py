"""
Change the IP addresses of the given hosts.

Uses https://github.com/micahjmartin/detcord to interact with the remote hosts
"""
from detcord import action, display

from networking import getRandomIps

env = dict()
env['user'] = 'root'
env['pass'] = 'changeme'
env['hosts'] = []  # DYNAMICALLY GENERATED IN getHosts()
env['silent'] = False
env['threading'] = True

NEWIPS = {}

@action
def update(host):
    """Update the IP addresses in workers.txt with a new, random IP
    """
    sudo = host.user != "root" # Only use sudo if we are not root
    display(host.local("echo Setting the IP to {}, sudo = {}".format(NEWIPS[host.host], sudo)))

def getHosts():
    """Read the workers IP addresses from a file"""
    with open("workers.txt") as fil:
        workers = [worker.strip() for worker in fil.readlines()]
    new_ips = getRandomIps(len(workers)) # Get a new Ip address for each worker
    for worker in workers:
        env['hosts'].append(worker)
        NEWIPS[worker] = new_ips.pop()
getHosts()


def on_detcord_end(detfile=""):
    print("Saving the new IP addresses:{}\n".format("\n".join(NEWIPS.values())))