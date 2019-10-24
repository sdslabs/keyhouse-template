import os
import sys
import hashlib
keys = {}
file = open("data/keys")
lines = file.readlines()
os.makedirs("api/names/")
for l in lines:
	idx = l.index('|')
	sshkey = l[idx+1:len(l)-1]
	sshkey = sshkey.split(' ')[0] + " " + sshkey.split(' ')[1]
	keys[l[:idx]] = hashlib.sha256(sshkey.encode()).hexdigest()
	f = open("api/names/{}".format(keys[l[:idx]]), "w")
	f.write(l[:idx])
	f.close()

def make_route(host, ruser, keyhash):
	if os.path.exists("api/access/{}/{}".format( host, ruser)) == False:
		os.makedirs("api/access/{}/{}".format(host, ruser))
	f = open("api/access/{}/{}/{}".format(host, ruser, keyhash), "w")
	f.write("1")
	f.close()

for hostname in os.listdir("data/hosts"):
	fp = open("data/hosts/{}".format(hostname))
	lines = fp.readlines()
	print(hostname)
	for l in lines:
		if l == '\n':
			continue
		idx = l.index('|')
		ruser = l[idx+1:len(l)-1]
		keyhash = keys[l[:idx]]
		make_route(hostname, ruser, keyhash)
