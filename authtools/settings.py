import pkg_resources

decrypt_dir = "/tmp/RAMSPACE/"

user_container = "ENCRYPTED_USER.zip"
card_container_dir = "ENCRYPTED_CARD.zip/"
user_container_enc = user_container + '.enc'
user_container_dec = user_container + '.dec'

usb_mount = "/mnt/keycard/"
serial_fname = "serial"
fprint_exec = "exec/" + "get_finger_temp"
fprint_exec_path = pkg_resources.resource_filename('authtools',fprint_exec)

pubkey_name = ".pubkey.pem"
serial_fname_enc = "serial.enc"

card_container = "ENCRYPTED_CARD.zip"
card_container_enc = card_container + ".enc"
card_container_dec = card_container + ".dec"

TCP_IP = '127.0.0.1'
TCP_PORT = 8888
BUFFER_SIZE = 1024

mindtct_exec = "/SRC/NBIS/Main/bin/mindtct"
bozorth3_exec = "/SRC/NBIS/Main/bin/bozorth3"

finger_temp = "finger.xyt"
hash_finger_temp = "hash_finger.xyt"
matching_score = "80"
user_cert = "user_cert.pem"
