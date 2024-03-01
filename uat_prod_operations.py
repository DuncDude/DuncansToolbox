import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import os

class UATProdOperations:
    def __init__(self, notebook):
        self.notebook = notebook

    def run_push_command(self):
        try:
            # Determine the selected folder from the dropdown menu
            selected_folder = self.folder_var.get()

            # If a folder is selected, start a new thread for git push
            if selected_folder:
                self.set_text(f"Pushing changes to folder {selected_folder}...")
                threading.Thread(target=self.perform_git_push, args=(selected_folder,), daemon=True).start()
            else:
                messagebox.showerror("Error", "Invalid folder selection.")
        except Exception as e:
            messagebox.showerror("Error", f"Command failed with error: {e}")

    def perform_git_push(self, selected_folder):
        try:
            # Push changes to the selected folder
            result = subprocess.check_output(["git", "push", selected_folder], text=True)

            # Display the output in the Text widget
            self.set_text(f"Pushed changes to folder {selected_folder} successfully:\n{result}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Command failed with error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def refresh_folder_options(self, *args):
        # Refresh the dropdown menu options
        working_directory = os.getcwd()
        folder_options = [folder for folder in os.listdir(working_directory) if os.path.isdir(os.path.join(working_directory, folder))]

        if folder_options:
            self.folder_var.set(folder_options[0])
            menu = self.folder_menu["menu"]
            menu.delete(0, "end")
            for folder in folder_options:
                menu.add_command(label=folder, command=tk._setit(self.folder_var, folder))
        else:
            self.folder_var.set("No folders found")

    def setup_uat_prod_tab(self):
        push_frame = tk.Frame(self.notebook)

        # Create a dropdown menu with folder names in the working directory
        working_directory = os.getcwd()
        self.folder_var = tk.StringVar()
        folder_options = [folder for folder in os.listdir(working_directory) if os.path.isdir(os.path.join(working_directory, folder))]
        self.folder_var.set(folder_options[0] if folder_options else "No folders found")
        self.folder_var.trace_add("write", self.refresh_folder_options)  # Call refresh_folder_options when folder_var changes
        self.folder_menu = tk.OptionMenu(push_frame, self.folder_var, *folder_options)
        self.folder_menu.pack(side=tk.TOP, pady=20)

        # Create a Text widget to display the output
        global text_widget_push  # Making it global to access in the main file
        text_widget_push = tk.Text(push_frame, height=10, width=60)
        text_widget_push.pack(side=tk.TOP, pady=20)

        # Create a Button to run the git push command
        push_button = tk.Button(push_frame, text="Run git push", command=self.run_push_command)
        push_button.pack(side=tk.TOP, pady=20)

        self.notebook.add(push_frame, text="Push to UAT/PROD")

def set_text(message):
    # Clear previous output and set the new message
    text_widget_push.delete(1.0, tk.END)
    text_widget_push.insert(tk.END, message)
