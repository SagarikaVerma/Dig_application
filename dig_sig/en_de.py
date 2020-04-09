from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from cryptography.fernet import Fernet
bp = Blueprint('en_de', __name__)

def encrypt_image():
	key = Fernet.generate_key()
	file=open('key.key','rb')
	key=file.read()
	file.close()

	in_file='buffer.jpg'
	out_file='test.encrypted'

	with open(in_file,'rb') as fo:
		data=fo.read()

	fernet=Fernet(key)
	encrypted=fernet.encrypt(data)

	with open(out_file, 'wb') as f:
		f.write(encrypted)

def decrypt_image():
	file = open('key.key', 'rb')
	key = file.read() # The key will be type bytes
	file.close()

	input_file = 'test.encrypted'
	output_file = 'dec2.jpg'

	with open(input_file, 'rb') as f:
 	   data = f.read()

	fernet = Fernet(key)
	encrypted = fernet.decrypt(data)

	with open(output_file, 'wb') as f:
   		f.write(encrypted)

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
