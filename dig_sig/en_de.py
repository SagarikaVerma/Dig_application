from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from cryptography.fernet import Fernet
bp = Blueprint('en_de', __name__)

def encrypt_image(image_path):
	key = Fernet.generate_key()
	
	in_file=image_path
	out_file='test.encrypted'

	with open(in_file,'rb') as fo:
		data=fo.read()

	fernet=Fernet(key)
	encrypted=fernet.encrypt(data)

	with open(out_file, 'wb') as f:
		f.write(encrypted)
	print (key)
	return key

def decrypt_image(de_key):
	input_file = 'test.encrypted'
	output_file = 'dec2.png'

	with open(input_file, 'rb') as f:
		data = f.read()

	fernet = Fernet(de_key)
	encrypted = fernet.decrypt(data)

	with open(output_file, 'wb') as f:
		f.write(encrypted)

	print("Done")

def encrypt_data():
	key = Fernet.generate_key()
	print (key)
	file = open('key.key', 'wb')
	file.write(key)
	file.close()

	file = open('key.key', 'rb')
	key = file.read()
	file.close()

	input_file = 'ec1.txt'
	output_file = 'ec1.encrypted'

	with open(input_file, 'rb') as f:
	    data = f.read()

	fernet = Fernet(key)
	encrypted = fernet.encrypt(data)

	with open(output_file, 'wb') as f:
	    f.write(encrypted)

def decrypt_data():
	file = open('key.key', 'rb')
	key = file.read() # The key will be type bytes
	file.close()

	input_file = 'ec1.encrypted'
	output_file = 'dc1.txt'

	with open(input_file, 'rb') as f:
		data = f.read()

	fernet = Fernet(key)
	encrypted = fernet.decrypt(data)

	with open(output_file, 'wb') as f:
		f.write(encrypted)
