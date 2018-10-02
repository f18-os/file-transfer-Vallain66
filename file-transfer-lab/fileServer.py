#! /usr/bin/env python3

import sys, re, socket
sys.path.append("../lib")       # for paramsx`
import params

CHUNK_SIZE = 100

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)

print("listening on:", bindAddr)

sock, addr = lsock.accept()

filename = sock.recv(CHUNK_SIZE)   			# recieving the file name
filecopy = "copy" + filename.decode()		# new name to avoid conflicts	
with open(filecopy, 'wb') as outf:
	while True:
		chunk = sock.recv(CHUNK_SIZE)
		print("Receiving...")
		if not chunk:
			break
		outf.write(chunk)
	sock.close()
