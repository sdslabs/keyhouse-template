import os
import sys
import json
import hashlib


def is_valid_username(username):
    if len(username) == 0:
        return False

    first = username[0]

    if not (('a' <= first <= 'z') or first == '_'):
        return False

    for ch in username:
        if not (('a' <= ch <= 'z') or ('0' <= ch <= '9') or ch == '_' or ch == '-'):
            return False

    return True


keys = {}
root = "./data/keys/"
usernames = os.listdir(root)

with open("config.json", "r") as f:
    config = json.load(f)
allowed_hosts = set(config.get("hosts", []))

os.makedirs("api/names/")

valid = True

for username in usernames:
    if not is_valid_username(username):
        print("Error: invalid username \"{}\" in data/keys/".format(username), file=sys.stderr)
        valid = False
        continue

    f = open(root + username, "r")
    sshkey = f.read()
    f.close()

    parts = sshkey.split(' ')
    if len(parts) < 2:
        print("Error: ssh key for \"{}\" must have at least 2 parts".format(username), file=sys.stderr)
        valid = False
        continue

    sshkey = parts[0] + " " + parts[1]
    keys[username] = hashlib.sha256(sshkey.encode()).hexdigest()
    f = open("api/names/{}".format(keys[username]), "w")
    f.write(username)
    f.close()


def make_route(host, ruser, keyhash):
    if os.path.exists("api/access/{}/{}".format(host, ruser)) == False:
        os.makedirs("api/access/{}/{}".format(host, ruser))
    f = open("api/access/{}/{}/{}".format(host, ruser, keyhash), "w")
    f.write("1")
    f.close()


for username in os.listdir("data/hosts"):
    if not is_valid_username(username):
        print("Error: invalid username \"{}\" in data/hosts/".format(username), file=sys.stderr)
        valid = False
        continue

    if username not in keys:
        print("Error: no key on file for username \"{}\"".format(username), file=sys.stderr)
        valid = False
        continue

    fp = open("data/hosts/{}".format(username))
    lines = fp.readlines()
    for l in lines:
        if l == '\n':
            continue
        l = l.strip()

        if '|' not in l:
            print("Error: malformed line \"{}\" in data/hosts/{} (expected \"host|user\")".format(l, username), file=sys.stderr)
            valid = False
            continue

        idx = l.index('|')
        hostname = l[:idx]
        ruser = l[idx+1:]

        if not hostname or not ruser:
            print("Error: malformed line \"{}\" in data/hosts/{} (expected \"host|user\")".format(l, username), file=sys.stderr)
            valid = False
            continue

        if not is_valid_username(ruser):
            print("Error: invalid remote group/user \"{}\" (from data/hosts/{})".format(ruser, username), file=sys.stderr)
            valid = False
            continue

        keyhash = keys[username]

        if hostname not in allowed_hosts:
            print("Error: host \"{}\" (from data/hosts/{}) is not in config.json".format(hostname, username), file=sys.stderr)
            valid = False
            continue

        make_route(hostname, ruser, keyhash)

if not valid:
    sys.exit(1)