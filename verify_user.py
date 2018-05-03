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
import authtools.settings
import os, sys
import hashlib

##
#Variables#

decrypt_dir = authtools.settings.decrypt_dir

user_container = authtools.settings.user_container
card_container_dir = authtools.settings.card_container_dir
user_container_enc = authtools.settings.user_container_enc
user_container_dec = authtools.settings.user_container_dec

finger_temp = authtools.settings.finger_temp
##
# Get user Pin
pin = input("Please enter your pin: ")
print(pin)

# Hash user pin 
hashed_pin = authtools.pintools.hashPin(pin)
print(hashed_pin)

# Decrypt container using hashed pin
authtools.cardtools.decryptContainerAES(\
        hashed_pin,\
        decrypt_dir +card_container_dir + user_container_enc,\
        decrypt_dir + user_container_dec)
# Extract the decrypted user container
authtools.cardtools.openZip(\
        decrypt_dir + user_container_dec,\
        decrypt_dir + user_container)

# Hash the template
print(decrypt_dir + user_container)
temp_hash_obj = hashlib.sha256()
with open("/tmp/RAMSPACE/ENCRYPTED_USER.zip/finger.xyt","rb") as f:
    for block in iter(lambda: f.read(65536), b''):
        sha256.update(block)
temp_hash = temp_hash_obj.hexdigest()
# Compare with hash on card
f = open("/tmp/RAMSPACE/ENCRYPTED_USER.zip/hash_finger.xyt","r")
user_temp_hash = f.read()
if(user_temp_hash == temp_hash):
    print("Hashes still match. Sending data to user database.")
else:
    print("Hashes did not match. Aborting process.")
    sys.exit()
# Encrypt/sign hash with private key on card
user_pem_file = open("/tmp/RAMSPACE/ENCRYPTED_USER.zip/user_cert.pem")
user_pem_obj = RSA.importKey(user_pem_key)
signed_user_hash = authtools.certtools.sign(temp_hash,user_pem_obj)
# Database responds with match or not
response = authtools.certtools.verifyHash(signed_user_hash)
if response:
    print("Template verified")
else:
    print("Template not verified")
# Scan user finger and compare 
# with template on card and store in secure space
authtools.biotools.getTemplate(decrypt_dir)
# Voter verified if fingerprint matches template
matching_score = authtools.biotools.compareTemplates(\
        decrypt_dir,decrypt_dir + finger_temp)
if authtools.settings.matching_score <= matching_score:
    print("User was verified")
else:
    print("User verification failed")
    sys.exit()
