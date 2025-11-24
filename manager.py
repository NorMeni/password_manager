import os
import base64
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generate_and_store_key():
	if not os.path.isfile("secret.key"):
		key = Fernet.generate_key()
		with open("secret.key", "w") as f:
			f.write(key)
		return key
	return None

def load_key():
	try:
		with open("secret.key", "r") as f:
			bytes = f.read()
		return bytes
	except FileNotFoundError:
		print("Key not found.")

def initialize_vault():
	key = generate_and_store_key()
	vault = []
	encrypt_vault(vault, key)

def decrypt_vault():
	key = load_key()
	with open("vault.dat", "rb") as f:
		encrypted_data = f.read()
	cypher_suite = Fernet(key)
	decrypted_data = cipher_suite.decrypt(encrypted_data)

def encrypt_vault(vault_data, key):
	
