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
	# the character used for padding
	# used to ensure that your value is always a multiple of BLOCK_SIZE
	PADDING = '$'
	# function to pad the functions. Lambda
	# is used for abstraction of functions.
	# basically, its a function, and you define it, followed by the param
	# followed by a colon,
	# ex = lambda x: x+5
	pad = lambda s: s + ((BLOCK_SIZE - len(s)) % BLOCK_SIZE) * PADDING
	# encrypt with AES, encode with base64
	#EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
	EncodeAES = lambda c, s: c.encrypt(pad(s))
	# generate a randomized secret key with urandom
	
	
	# creates the cipher obj using the key
	cipher = AES.new(encryptKey)
	# encodes you private info!
	encoded = EncodeAES(cipher, privateInfo)
	#secret =  base64.b64encode(secret)
	return encoded
	#print secret.encode("string-escape")
	#print 'Encrypted string:', encoded
	#print 'encryption key:', base64.b64encode(encryptKey)
	
	#return (encoded, secret)

'''key = os.urandom(16)
text = "123456789"
final = encryption(text,key)

print type(final)
print final'''


def decryption(encryptedString, key):
	#print "hi"
	PADDING = '$'
	DecodeAES = lambda c, e: c.decrypt(e).rstrip(PADDING)
	#Key is FROM the printout of 'secret' in encryption
	#below is the encryption.
	encryption = encryptedString
	print base64.b64encode(encryption)
	cipher = AES.new(key)
	decoded = DecodeAES(cipher, encryption)
	#print type(decoded)
	print base64.b64encode(decoded)

	return decoded
'''
key = os.urandom(16)
text = "1234567891234567"
e_text = encryption(text, key)
print base64.b64encode(e_text)
print base64.b64encode(key)
print decryption(e_text, key)
#print r'''