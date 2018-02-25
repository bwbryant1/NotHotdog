"""
-->Verify card
i.	Plug in keycard
ii.	Pull card container off card - all data encapsulated creates a container - copy to RAM
iii.	On card container will be serial number in plane text
iv.	Send serial number to card database and return corresponding symmetric key
v.	Use symmetric key to decrypt AES 
vi.	Pull public key
vii.	Voting poll encrypt serial number with public key
viii.	Send encrypted serial number to card database
ix.	Data base will decrypt with private key
x.	Compare serial numbers 
xi.	Send back if verified or not 

"""

import authtools.usbtools
import authtools.cardtools
import authtools.certtools
import Crypto.PublicKey.RSA
import hashlib
import socket
import ssl 
import sys 




##
#variables#
decrypt_dir = "/tmp/RAMSPACE/"
usb_mount = "/mnt/keycard/"
serial_fname = "serial"

pubkey_name = ".pubkey.pem"
serial_fname_enc = "serial.enc"

card_container = "ENCRYPTED_CARD.zip"
card_container_enc = card_container + ".enc"
card_container_dec = card_container + ".dec"

TCP_IP = '10.0.0.78'
TCP_PORT = 8888
BUFFER_SIZE = 1024
##

usb = authtools.usbtools.waitForPlug()

if usb:
    usb.mount()

print(usb.listFiles())
if authtools.cardtools.detectContainer(usb):
    print("Found Container!")
    serial_file = open(usb_mount + serial_fname)
    serial = serial_file.read()
    print(serial)
else:
    print("no container")
sym_key = authtools.certtools.get_symkey_from_serial(serial)
hashed_sym_key = hashlib.sha256(sym_key.encode()).digest()

authtools.cardtools.decryptContainerAES(\
        hashed_sym_key, \
        usb_mount + card_container_enc,\
        decrypt_dir + card_container_dec\
        )

authtools.cardtools.openZip(\
        decrypt_dir + card_container_dec,\
        decrypt_dir + card_container)

card_pubkey_file = open(decrypt_dir + card_container + '/' + serial + pubkey_name)
card_pubkey = card_pubkey_file.read()
print(card_pubkey)
card_pubkey_obj = Crypto.PublicKey.RSA.importKey(card_pubkey)

serial_encrypted = card_pubkey_obj.encrypt(serial.encode(encoding='UTF-8'),32)
serial_encrypted_file = open(decrypt_dir + serial_fname_enc ,'w+')
serial_encrypted_file.write(str(serial_encrypted))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
ss = ssl.wrap_socket(s)
#ss = ssl(s)

print (ss.read(BUFFER_SIZE))
ss.write(serial.encode())
response = ss.read(65535)
print(response)
ss.write(str(serial_encrypted).encode())
response = ss.read(65535)
print(response)
s.close()


serial_encrypted_file.close()
card_pubkey_file.close()
usb.unmount()
