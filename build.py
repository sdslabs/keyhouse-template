"""
This along-with gh-pages hosts a static website which watchdog uses to check
if the person has access to ssh on the machine running watchdog.
"""

import os
import hashlib


API_ACCESS = "api/access"
API_NAMES = "api/names"
DATA_KEYS = "data/keys"
DATA_HOSTS = "data/hosts"


def make_route(host, ruser, keyhash):
    if os.path.exists("{}/{}/{}".format(API_ACCESS, host, ruser)) is False:
        os.makedirs("{}/{}/{}".format(API_ACCESS, host, ruser))
    f = open("{}/{}/{}/{}".format(API_ACCESS, host, ruser, keyhash), "w")
    f.write("1")
    f.close()


keys = {}

file = open(DATA_KEYS)
lines = file.readlines()
file.close()

os.makedirs("{}/".format(API_NAMES))

for line in lines:
    idx = line.index("|")
    sshkey = line[idx + 1: len(line) - 1]
    sshkey = "{} {}".format(sshkey.split(" ")[0], sshkey.split(" ")[1])
    keys[line[:idx]] = hashlib.sha256(sshkey.encode()).hexdigest()
    f = open("{}/{}".format(API_NAMES, keys[line[:idx]]), "w")
    f.write(line[:idx])
    f.close()

for hostname in os.listdir(DATA_HOSTS):
    fp = open("{}/{}".format(DATA_HOSTS, hostname))
    lines = fp.readlines()
    fp.close()
    for line in lines:
        if line == "\n":
            continue
        idx = line.index("|")
        ruser = line[idx + 1: len(line) - 1]
        keyhash = keys[line[:idx]]
        make_route(hostname, ruser, keyhash)
