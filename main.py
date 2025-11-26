import manager as pm

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
vault.append(new_entry)
pm.encrypt_vault(vault, key)
print(vault)

