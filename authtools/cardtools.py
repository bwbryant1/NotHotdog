import os
import random
import struct
import zipfile
import shutil
from Crypto.Cipher import AES
import authtools.usbtools
def encryptContainerAES(key, in_filename, out_filename=None, chunksize=64*1024):
    """ Encrypts a file using AES (CBC mode) with the
        given key.

        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.

        in_filename:
            Name of the input file

        out_filename:
            If None, '<in_filename>.enc' will be used.

        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = os.urandom(AES.block_size)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    length = 16 - (len(chunk) % 16)
                    chunk += bytes([length])*length

                outfile.write(encryptor.encrypt(chunk))


def decryptContainerAES(key, in_filename, out_filename=None, chunksize=24*1024):
    """ Decrypts a file using AES (CBC mode) with the
        given key. Parameters are similar to encrypt_file,
        with one difference: out_filename, if not supplied
        will be in_filename without its last extension
        (i.e. if in_filename is 'aaa.zip.enc' then
        out_filename will be 'aaa.zip')
    """
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                #print(len(chunk))
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)

def detectContainer(usb,conDir=None):
    container_name = ['identity.id']
    
    if isinstance(usb,authtools.usbtools.USB):
        pass
    else:
        return
    
    if not conDir:
        conPath = '/mnt/keycard'
    else:
        conDir = conDir

    for _file in usb.listFiles():
        if _file in container_name:
            return True
    return False
    
def openZip(zipPath,zipEPath):
    with zipfile.ZipFile(zipPath,"r") as zip_ref:
        zip_ref.extractall(zipEPath)
    
def zipFolder(folderPath,zipPath):
    shutil.make_archive(zipPath, 'zip', folderPath)
