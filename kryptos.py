from Crypto.Cipher import AES
from Crypto.Cipher import DES
from Crypto.PublicKey import RSA
from Crypto import Random
#base64 is used for encoding. dont confuse encoding with encryption#
#encryption is used for disguising data
#encoding is used for putting data in a specific format
import base64
# os is for urandom, which is an accepted producer of randomness that
# is suitable for cryptology.
import os

def encryptAES(plaintext, key):
	BLOCK_SIZE = 16
	padding = "@"
	plaintext = plaintext + ((BLOCK_SIZE - len(plaintext)) % BLOCK_SIZE) * padding
	cipherkey = AES.new(key)
	ciphertext = cipherkey.encrypt(plaintext)
	return ciphertext

def decryptAES(ciphertext, key):
	BLOCK_SIZE = 16
	padding = "@"
	cipherkey = AES.new(key)
	plaintext = cipherkey.decrypt(ciphertext)
	plaintext = plaintext.rstrip(padding)
	return plaintext



def encryptDES(plaintext, key):
	BLOCK_SIZE = 8
	padding = "@"
	plaintext = plaintext + ((BLOCK_SIZE - len(plaintext)) % BLOCK_SIZE) * padding
	print plaintext
	cipherkey = DES.new(key)
	ciphertext = cipherkey.encrypt(plaintext)
	return ciphertext

def decryptDES(ciphertext, key):
	BLOCK_SIZE = 8
	padding = "@"
	cipherkey = DES.new(key)
	plaintext = cipherkey.decrypt(ciphertext)
	plaintext = plaintext.rstrip(padding)
	return plaintext



def encryptRSA(plaintext, key):
	BLOCK_SIZE = 8
	padding = "@"
	public_key = key.publickey()
	enc_data = public_key.encrypt(plaintext,32)[0]
	return enc_data

def decryptRSA(ciphertext, key):
	plaintext = key.decrypt(ciphertext)
	return plaintext


key = os.urandom(8)
#random_generator = Random.new().read
#key = RSA.generate(2048, random_generator)
text = "1234567891234567"
e_text = encryptDES(text, key)
#print "key: ", base64.b64encode(key)
print "encrypted text: ", base64.b64encode(e_text)
print decryptDES(e_text, key)
