"""
-->Verify user
i.	Input PIN
ii.	Hash PIN - with SHA256 - 32 bytes (256 bits)
iii.	Decrypt user container using the 256 bits from pin hash with AES decrypt
iv.	Now can see template hash
v.	Locally rehash template on card to make sure it match the hash on card. This hash should also match the user database hash 
vi.	Hashed Template Sent to user Federal Database encrypted with user private key that's on card within user container
vii.	User database will decrypt with public key
viii.	Compare with hash on database
ix.	Matches, then its okay to scan thumbprint
 
10.	Scan Fingerprint
11.	Create template
12.	Verify Template that you scanned against the one on card
xiii.	Voter verified
 
xiv.	Delete and write 1s to all data on RAM
"""
import authtools.pintools
import authtools.cardtools
import os
##
#Variables#

decrypt_dir = "/tmp/RAMSPACE/"

user_container = "ENCRYPTED_USER.zip"
card_container_dir = "ENCRYPTED_CARD.zip/"
user_container_enc = user_container + '.enc'
user_container_dec = user_container + '.dec'

##

pin = input("Please enter your pin: ")
print(pin)

hashed_pin = authtools.pintools.hashPin(pin)
print(hashed_pin)

authtools.cardtools.decryptContainerAES(\
        hashed_pin,\
        decrypt_dir +card_container_dir + user_container_enc,\
        decrypt_dir + user_container_dec)

authtools.cardtools.openZip(\
        decrypt_dir + user_container_dec,\
        decrypt_dir + user_container)
