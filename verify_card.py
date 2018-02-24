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
import Crypto.PublicKey.RSA


##
#variables#
decrypt_dir = "/tmp/RAMSPACE/"
usb_mount = "/mnt/keycard/"
serial_fname = "serial"

pubkey_name = ".pubkey.pem"

card_container = "ENCRYPTED_CARD"
card_container_enc = card_container + ".enc"
card_container_dec = card_container + ".dec"
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

#sym_key = authtools.certtools.get_symkey_from_serial(serial):

authtools.cardtools.decryptContainerAES(sym_key,card_container_enc,decrypt_dir + card_container_dec)
card_pubkey_file = open(decrypt_dir + card_container + '/' + serial + pubkey_name)
card_pubkey = Crypto.PublicKey.RSA.importKey(card_pubkey_file.read())

serial_encrypted = card_pubkey.encrypt(serial,32)


usb.unmount()
