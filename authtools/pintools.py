import hashlib
import binascii
import sys, os 
from Crypto.Cipher import AES

#Function Declaration for hash
def hashPin(p):
	pin = str(p)
	del(p)
	length = len(pin)
	if length != 5 or not pin.isdigit():
		del(pin)
		del(length)
		print("ERROR: Invalid PIN")
		return	
	h = hashlib.sha256()
	h.update(pin.encode())
	#print(h.digest())
	return h.digest()
	del(h)
