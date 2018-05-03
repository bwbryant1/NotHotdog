'''
    Simple socket server using threads
'''
 
import socket
import sys
from _thread import *
from hashlib import sha256 
from OpenSSL import SSL
from executables import make_sql
import ast
from Crypto.PublicKey import RSA

"""
MySQL bits
"""
con = make_sql()
"""
End MySQL
"""
 
HOST = '0.0.0.0'  
PORT = 8888

BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file('key')
context.use_certificate_file('cert')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s = SSL.Connection(context, sock)
print('Socket created')
 

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
     
print('Socket bind complete')
 

s.listen(10)
print('Socket now listening')

def clientthread(conn):

    conn.send("You have connected to the Keycard Verification Server")  # echo
    while True:

        data = ''
        try:
            data = conn.recv(BUFFER_SIZE)
        except:
           print('disconnected with ' + addr[0] + ':' + str(addr[1]))
        if not data: break
        data = data.rstrip("\n".encode())
        serial = data.decode()
        print("I recv'd this in plaintext: " + serial)
        conn.send('Ready to recv file')
        enc = conn.recv(BUFFER_SIZE)
        enc = enc.decode()
        print("I recd this encoded:" + enc)
        priv_key_file = open("../authtools/data/keycard_certs/1108170000001068.key.pem")
        priv_key = priv_key_file.read()
        #print(priv_key)
        priv_key_obj = RSA.importKey(priv_key)
        dec = priv_key_obj.decrypt(ast.literal_eval(str(enc)))
        print("I just decoded: " + dec.decode())
        if dec.decode() == serial:
            conn.send("sent serial matches decrypted text and cert is valid. Verified")
        else:
            conn.send("Verification failed")
        print("\n")
    conn.close()

while 1:
    
    conn, addr = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))
     
    
    start_new_thread(clientthread ,(conn,))
 
s.close()
