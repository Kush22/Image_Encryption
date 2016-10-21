from Crypto.Cipher import AES
from Crypto.Cipher import DES
from Crypto.PublicKey import RSA
from Crypto import Random
import base64
import os

def encryptAES(plaintext, key):
	BLOCK_SIZE = 16
	padding = "@"
	plaintext = plaintext + ((BLOCK_SIZE - len(plaintext)) % BLOCK_SIZE) * padding
	cipherkey = AES.new(key)
	ciphertext = cipherkey.encrypt(plaintext)
	return ciphertext


def decryptAES(ciphertext, key):
	cipherkey = AES.new(key)
	plaintext = cipherkey.decrypt(ciphertext)
	return plaintext


def encryptDES(plaintext, key):
	BLOCK_SIZE = 8
	padding = "@"
	plaintext = plaintext + ((BLOCK_SIZE - len(plaintext)) % BLOCK_SIZE) * padding
	cipherkey = DES.new(key)
	ciphertext = cipherkey.encrypt(plaintext)
	return ciphertext


def decryptDES(ciphertext, key):
	cipherkey = DES.new(key)
	plaintext = cipherkey.decrypt(ciphertext)
	return plaintext


def encryptRSA(plaintext, key):
	BLOCK_SIZE = 8
	padding = "@"
	enc_data = key.encrypt(plaintext,32)[0]
	return enc_data
	

def decryptRSA(ciphertext, key):
	plaintext = key.decrypt(ciphertext)
	return plaintext


if __name__=="__main__":
	key = os.urandom(8)
	#random_generator = Random.new().read
	#key = RSA.generate(2048, random_generator)
	text = "1234567891234567"
	e_text = encryptDES(text, key)
	#print "key: ", base64.b64encode(key)
	print "encrypted text: ", base64.b64encode(e_text)
	print decryptDES(e_text, key)
