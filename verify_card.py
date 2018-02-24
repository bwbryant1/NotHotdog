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

usb = authtools.usbtools.waitForPlug()

if usb:
    usb.mount()

if authtools.cardtools.detectContainer(usb):
    print("Found Container!")

