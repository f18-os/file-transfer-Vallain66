
UPDATED: 9/19/18

## fileServer.py
## fileClient.py
* TEST: N/a

* COMPILE: N/a

* TO RUN: ./fileServer.py    AND   ./fileClient.py

## PRINCIPLE OF OPERATION:
fileServer.py:
	
* a socket is created on address 127.0.0.1 and port 50001 
* the socket is set to listen and block until a connection is accepted
* the first thing recieved is the file's name
  * the files name is appended with "copy" to the front if the files name to designate it is a copy
* the server will receive in batches of 100 bytes which is instantiated as CHUNK_SIZE
* the server will write to the copy until no data is sent
* once no data is setn the socket is closed

fileClient.py:

* a socket is created and connected to 127.0.0.1 on port 50001
* if the connection is successful the client requests the name of the file to "put" on the server
* the client checks if the file exists on the current path and will close the socket and  exits if it doesn't
* the size of the file is determined, if its an empty file an error is thrown, socket is closed and program exits
* if the file both exists and is not empty the files name is sent to the server
* the file is read in batches of 100 bytes which is instantiated as CHUNK_SIZE
* each chunk is sent in turn, once completed the socket is closed
