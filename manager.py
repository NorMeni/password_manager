import os
import base64
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generate_and_store_key():
	if not os.path.isfile("secret.key"):
		key = Fernet.generate_key()
		with open("secret.key", "wb") as f:
			f.write(key)
		print(f"Generated key: {key}")
		return key
	else:
		with open("secret.key", "rb") as f:
			key = f.read()
		#print(f"Loaded existing key: {key}")
		return key

def load_key():
	if os.path.exists("secret.key"):
		with open("secret.key", "rb") as f:
			return f.read()
	else:
		raise FileNotFoundError("Key not found.")

def initialize_vault():
	key = generate_and_store_key()

	if not os.path.exists("vault.dat"):
		vault = []
		encrypt_vault(vault, key)
	return key

def decrypt_vault():
	key = load_key()
	if os.path.exists("vault.dat"):
		with open("vault.dat", "rb") as f:
			encrypted_data = f.read()
	else:
		raise FileNotFoundError("Vault not found.")

	cipher = Fernet(key)
	decrypted_data = cipher.decrypt(encrypted_data)
	return json.loads(decrypted_data)

def encrypt_vault(vault_data, key):
	#print(f"ENCRYPTING: {len(vault_data)} entries: {vault_data}")
	json_string = json.dumps(vault_data)
	cypher = Fernet(key)
	encrypted_data = cypher.encrypt(json_string.encode('utf-8'))
	with open("vault.dat", "wb") as f:
		f.write(encrypted_data)
