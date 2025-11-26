import manager as pm
import os
import json

key = pm.initialize_vault()
#verify that secret.key and vault.dat were created

vault = pm.decrypt_vault()
print(vault)
#expected output: []

new_entry = {
	"service": "Test service",
	"username": "Test username",
	"password": "test_pass",
	"notes": "this is just a test"
}

if os.path.exists("test_file.JSON"):
	with open("test_file.JSON", "r") as f:
		vault_info = json.load(f)
vault.extend(vault_info)

pm.encrypt_vault(vault, key)
print(vault)

