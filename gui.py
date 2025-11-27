import tkinter as tk
from tkinter import ttk
import manager as pm

class PasswordManagerApp:
	def __init__(self):
		self.key = pm.load_key()
		self.vault = pm.decrypt_vault()

	def on_add_entry(self, listbox, dialogue, service, username, password, notes):
		new_entry = {
			"service": service,
			"username": username,
			"password": password,
			"notes": notes
		}
		self.vault.append(new_entry)
		pm.encrypt_vault(self.vault, self.key)
		self.refresh_vault_display(listbox)
		dialogue.destroy()

	def refresh_vault_display(self, listbox):
		display_vault = []

		if len(self.vault) == 0:
			display_vault.append("No entries")
		else:
			for item in self.vault:
				display_vault.append(f"{item["service"]} - {item["username"]}")

		listbox.delete(0, tk.END)
		for item in display_vault:
			listbox.insert(tk.END, item)

	def open_add_dialogue(self, app, listbox):
		dialogue = tk.Toplevel()
		dialogue.title('Please enter new entry')
		dialogue.geometry('400x400')

		service_entry = tk.Entry(dialogue)
		tk.Label(dialogue, text='Service:').grid(row=0, column=0, sticky="w", padx=5, pady=5)
		service_entry.grid(row=0, column=1, padx=5, pady=5)

		username_entry = tk.Entry(dialogue)
		tk.Label(dialogue, text="Username:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
		username_entry.grid(row=1, column=1, padx=5, pady=5)

		password_entry = tk.Entry(dialogue, show="*")
		tk.Label(dialogue, text="Password:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
		password_entry.grid(row=2, column=1, padx=5, pady=5)

		notes_entry = tk.Text(dialogue, height=4, width=30)
		tk.Label(dialogue, text="Notes:").grid(row=3, column=0, sticky="nw", padx=5, pady=5)
		notes_entry.grid(row=3, column=1, padx=5, pady=5)

		save_button = tk.Button(
			dialogue,
			text='Save',
			command=lambda: self.on_add_entry(listbox, dialogue, service_entry.get(), username_entry.get(), password_entry.get(), notes_entry.get("1.0", tk.END).strip())
		)
		save_button.grid(row=4, column=0, columnspan=2, pady=10)

def setup_gui():
	root = tk.Tk()
	root.title("Password Manager")

	window_width = 800
	window_height = 600

	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()

	center_x = int(screen_width/2 - window_width / 2)
	center_y = int(screen_height/2 - window_height / 2)

	root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

	app = PasswordManagerApp()

	label = ttk.Label(
		root,
		text='List of services'
	)
	label.pack(padx=10, pady=0, side=tk.TOP, fill=tk.X)

	#initialize list as empty
	listbox = tk.Listbox(root)
	listbox.pack()
	app.refresh_vault_display(listbox)

	listbox.pack(padx=10, pady=10, expand=True, fill=tk.BOTH, side=tk.LEFT)

	#button
	add_button = tk.Button(
		root,
		text="Add Entry",
		command=lambda: app.open_add_dialogue(app, listbox)
	)
	add_button.pack()

	root.mainloop()
