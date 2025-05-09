import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os
from tkinterdnd2 import DND_FILES, TkinterDnD

class ModelCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Model Creator Interface")

        # Table to display Name and Model
        self.tree = ttk.Treeview(root, columns=("Name", "Model"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Model", text="Model")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Buttons
        self.create_button = tk.Button(root, text="Create", command=self.create_models)
        self.create_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.refresh_button = tk.Button(root, text="Refresh", command=self.refresh_table)
        self.refresh_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Drag and Drop functionality
        self.tree.drop_target_register(DND_FILES)
        self.tree.dnd_bind('<<Drop>>', self.on_drop)

        self.modelfiles = []

    def on_drop(self, event):
        # Handle file drop event
        files = self.tree.tk.splitlist(event.data)
        print("Dropped files:", files)  # Debug statement
        for filepath in files:
            if filepath.endswith('.modelfile'):
                self.add_modelfile(filepath)

    def add_modelfile(self, filepath):
        # Read the first line to get the model name
        print("Adding modelfile:", filepath)  # Debug statement
        try:
            with open(filepath, 'r') as file:
                first_line = file.readline().strip()
                if first_line.startswith("FROM "):
                    model_name = first_line[5:]
                    name = os.path.splitext(os.path.basename(filepath))[0]
                    self.modelfiles.append((name, model_name, filepath))
                    self.tree.insert("", "end", values=(name, model_name))
        except Exception as e:
            print(f"Error reading file {filepath}: {e}")

    def create_models(self):
        # Execute the ollama create command for each modelfile
        for name, model, filepath in self.modelfiles:
            command = f"ollama create {name} -f {filepath}"
            try:
                subprocess.run(command, shell=True, check=True)
                messagebox.showinfo("Success", f"Model {name} created successfully!")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to create model {name}: {e}")

    def refresh_table(self):
        # Clear the table and modelfiles list
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.modelfiles.clear()

if __name__ == "__main__":
    root = TkinterDnD.Tk()  # Use TkinterDnD.Tk() instead of tk.Tk()
    app = ModelCreatorApp(root)
    root.mainloop()
