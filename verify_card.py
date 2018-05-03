"""
-->Verify card
i.	Plug in keycard
ii.	Pull card container off card - all data encapsulated creates a container - copy to RAM
iii.	On card container will be serial number in plain text
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
import authtools.settings
import Crypto.PublicKey.RSA
import hashlib
import socket
import ssl 
import sys 
import os

##
#variables#
decrypt_dir = authtools.settings.decrypt_dir
usb_mount = authtools.settings.usb_mount
serial_fname = authtools.settings.serial_fname

pubkey_name = authtools.settings.pubkey_name
serial_fname_enc = authtools.settings.serial_fname_enc

card_container = authtools.settings.card_container
card_container_enc = authtools.settings.card_container_enc
card_container_dec = authtools.settings.card_container_dec

TCP_IP = authtools.settings.TCP_IP
TCP_PORT = authtools.settings.TCP_PORT
BUFFER_SIZE = authtools.settings.BUFFER_SIZE
##

# This monitors usb ports and block devices and waits for our USB
usb = authtools.usbtools.waitForPlug()

#when the usb object is created we mount it
if usb:
    usb.mount()
print(usb.listFiles())

#Here we are looking for a container on the card. The container will either be at a specific memory 
#   address or filename
if authtools.cardtools.detectContainer(usb):
    print("Found Container!")
    # since there is a container we need the serial number to request the symmetric key
    serial_file = open(usb_mount + serial_fname)
    serial = serial_file.read()
    print(serial)
else:
    print("no container")

# We request the symmetric key from the card center server    
sym_key = authtools.certtools.get_symkey_from_serial(serial)
# We hash the serial so it will match proper key length for AES
hashed_sym_key = hashlib.sha256(sym_key.encode()).digest()

# Here we decrypt the Card container using the hashed symmertric key
authtools.cardtools.decryptContainerAES(\
        hashed_sym_key, \
        usb_mount + card_container_enc,\
        decrypt_dir + card_container_dec\
        )

# Once the container is decrypted, we can open the container, which is a zip
authtools.cardtools.openZip(\
        decrypt_dir + card_container_dec,\
        decrypt_dir + card_container)

#The public key of the card can be read from the card container
card_pubkey_file = open(decrypt_dir + card_container + '/' + serial + pubkey_name)
card_pubkey = card_pubkey_file.read()
print(card_pubkey)
card_pubkey_obj = Crypto.PublicKey.RSA.importKey(card_pubkey)

# Here we encrypt the serial of the card with the RSA public key
serial_encrypted = card_pubkey_obj.encrypt(serial.encode(encoding='UTF-8'),32)
serial_encrypted_file = open(decrypt_dir + serial_fname_enc ,'w+')
serial_encrypted_file.write(str(serial_encrypted))

# We open a secure connection with the card server and send the encrypted serial
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
ss = ssl.wrap_socket(s)

# Read server hello
print (ss.read(BUFFER_SIZE))
# Send serial of the card (already been done, but we will do it again)
ss.write(serial.encode())
# Read the server response
response = ss.read(65535)
print(response)
# Send the encrypted data to the server
ss.write(str(serial_encrypted).encode())
# Read the response of the encrypted paylod
response = ss.read(65535)
print(response)
# Close server connection
s.close()

# perform file cleanup
os.system("rm -rf /tmp/RAMSPACE/*")
serial_encrypted_file.close()
card_pubkey_file.close()
usb.unmount()
