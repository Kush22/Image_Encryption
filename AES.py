from Crypto.Cipher import AES
#base64 is used for encoding. dont confuse encoding with encryption#
#encryption is used for disguising data
#encoding is used for putting data in a specific format
import base64
# os is for urandom, which is an accepted producer of randomness that
# is suitable for cryptology.
import os
def encryption(privateInfo, encryptKey):
	#32 bytes = 256 bits
	#16 = 128 bits
	# the block size for cipher obj, can be 16 24 or 32. 16 matches 128 bit.
	BLOCK_SIZE = 16
	EncodeAES = lambda c, s: c.encrypt(s)
	cipher = AES.new(encryptKey)
	# encodes you private info!
	encoded = EncodeAES(cipher, privateInfo)
	#secret =  base64.b64encode(secret)
	print "hello"
	return encoded


def decryption(encryptedString, key):
	
	DecodeAES = lambda c, e: c.decrypt(e)
	encryption = encryptedString
	cipher = AES.new(key)
	decoded = DecodeAES(cipher, encryption)
	return decoded
