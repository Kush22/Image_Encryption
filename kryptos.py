
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
	public_key = key.publickey()
	enc_data = public_key.encrypt(plaintext,32)[0]
	return enc_data

def decryptRSA(ciphertext, key):
	plaintext = key.decrypt(ciphertext)
	return plaintext

