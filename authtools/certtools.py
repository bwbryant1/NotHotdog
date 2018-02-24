import Crypto.PublicKey.RSA
import Crypto.Random
import MySQLdb as mdb

##
#variables#
host = '10.0.0.78'
port = 9006
user = 'brandon'
passwd = 'DBpass'
db = 'keycards'
##

def make_sql():
    con = mdb.connect(host=host,user=user,passwd=passwd,db=db,port=port)
    cur = con.cursor()
    return con,cur

def get_symkey_from_serial(serial):
    con,cur= make_sql()
    cur.execute("select symkey from cards where serial = {serial}".format(serial=serial))
    symkey_tuple = cur.fetchall()
    symkey = ''
    if len(symkey_tuple) > 0:
        symkey = symkey_tuple[0][0]
    return symkey

def make_rand_key():
    pass
def encrypt_with_pub_key(key):
    pass
def decrypt_wth_pub_key():
    pass
def encrypt_with_priv_key(key):
    pass
def decrypt_wth_priv_key():
    pass
