import manager as pm
import os
import json
import gui as gui


def main():
	key = pm.initialize_vault()
	vault = pm.decrypt_vault()
	gui.setup_gui(vault, key)

if __name__ == "__main__":
	main()
