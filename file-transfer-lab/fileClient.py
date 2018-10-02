#! /usr/bin/env python3

# Echo client program
import socket, sys, re, os

sys.path.append("../lib")       # for params
import params

CHUNK_SIZE = 100

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

filename = input("Put which file on server: ")
if not os.path.exists(filename):
	print ("File input %s doesn't exist! Exiting" % filename)
	s.close()
	exit()

if os.path.getsize(filename) > 0:
	s.send(bytes(filename, 'utf-8'))		# send the files name to use as output file name
	with open(filename, 'rb') as file:
		payload = file.read(CHUNK_SIZE)
		while payload:
			s.send(payload)
			payload = file.read(CHUNK_SIZE)
		fileCopyName = "copy" + filename
		print(fileCopyName, " was put on server")
	s.close()
else:
	print ("File input %s is empty! Exiting" % filename)
	s.close()
	exit()
