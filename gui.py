import tkinter as tk
from tkinter import ttk
import manager as pm

class PasswordManagerApp:
	def __init__(self):
		self.key = pm.load_key()
		self.vault = pm.decrypt_vault()

	def on_add_entry(self, treeview, dialogue, service, username, password):
		new_entry = {
			"service": service,
			"username": username,
			"password": password
		}
		self.vault.append(new_entry)
		pm.encrypt_vault(self.vault, self.key)
		self.refresh_vault_display(treeview)
		dialogue.destroy()

	def refresh_vault_display_defunct(self, listbox):
		display_vault = []

		if len(self.vault) == 0:
			display_vault.append("No entries")
		else:
			for item in self.vault:
				display_vault.append(f"{item["service"]} - {item["username"]}")

		listbox.delete(0, tk.END)
		for item in display_vault:
			listbox.insert(tk.END, item)
	def refresh_vault_display(self, treeview):
		display_vault = []

		if len(self.vault) == 0:
			display_vault.append("No entries")
		else:
			for item in treeview.get_children():
				treeview.delete(item)
			for item in self.vault:
				level1 = treeview.insert('', tk.END, text=f"{item["service"]}")
				treeview.insert(level1, tk.END, text="Username", values=(f"{item["username"]}"))
				treeview.insert(level1, tk.END, text="Password", values=(f"{item["password"]}"))

	def open_add_dialogue(self, app, treeview):
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

		#notes_entry = tk.Text(dialogue, height=4, width=30)
		#tk.Label(dialogue, text="Notes:").grid(row=3, column=0, sticky="nw", padx=5, pady=5)
		#notes_entry.grid(row=3, column=1, padx=5, pady=5)

		save_button = tk.Button(
			dialogue,
			text='Save',
			command=lambda: self.on_add_entry(treeview, dialogue, service_entry.get(), username_entry.get(), password_entry.get())
		)
		save_button.grid(row=4, column=0, columnspan=2, pady=10)

	def on_delete_entry(self, app, treeview):
		selected_items = treeview.selection()

		top_level_items = []
		for item in selected_items:
			if treeview.parent(item) == '':
				top_level_items.append(item)

		if not top_level_items:
			warning = tk.Toplevel()
			warning.title('Warning')
			warning.geometry('400x100')
			l = ttk.Label(warning, text = "Please select an entry to delete.")
			l.pack()
			ok_button = tk.Button(
				warning,
				text='OK',
				command=lambda:warning.destroy()
			)
			ok_button.pack()
		else:
			items = ""
			for entry in top_level_items:
				index = treeview.index(entry)
				service = self.vault[index]["service"]
				items += f"{service}, "

			warning = tk.Toplevel()
			warning.title('Warning')
			l = ttk.Label(warning, text = f"Are you sure you want to delete {items[:-2]}?")
			l.pack()

			no_button = tk.Button(
				warning,
				text='No',
				command=lambda:warning.destroy()
			)
			yes_button = tk.Button(
				warning,
				text='Yes',
				command=lambda: [warning.destroy(), self.delete_entries(treeview)]
			)
			no_button.pack()
			yes_button.pack()

	def delete_entries(self, treeview):
		selected_items = treeview.selection()

		items_to_delete = []
		for item in selected_items:
			index = treeview.index(item)
			items_to_delete.append(index)

		for index in sorted(items_to_delete, reverse=True):
			del self.vault[index]

		pm.encrypt_vault(self.vault, self.key)
		self.refresh_vault_display(treeview)
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
	#listbox = tk.Listbox(root)
	#listbox.pack()
	#app.refresh_vault_display(listbox)

	#listbox.pack(padx=10, pady=10, expand=True, fill=tk.BOTH, side=tk.LEFT)

	treeview = ttk.Treeview(columns=("Username", "Password"))
	app.refresh_vault_display(treeview)

	treeview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

	#button
	add_button = tk.Button(
		root,
		text="Add Entry",
		command=lambda: app.open_add_dialogue(app, treeview)
	)
	add_button.pack()

	#delete button
	del_button = tk.Button(
		root,
		text="Delete entry",
		command=lambda: app.on_delete_entry(app, treeview)
	)
	del_button.pack()

	root.mainloop()
