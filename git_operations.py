import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import os
import shutil

class GitOperations:
    def __init__(self, notebook):
        self.notebook = notebook

    def run_clone_command(self):
        try:
            # Determine the selected repository from the dropdown menu
            selected_repo = self.repo_var.get()

            # Map the selected repository to the corresponding GitHub URL
            repo_urls = {
                "UI-Core": "https://github.com/DarkFlippers/unleashed-firmware",
                "Backend-Core": "https://github.com/DarkFlippers/Multi_Fuzzer"
            }

            # Get the GitHub URL for the selected repository
            repo_url = repo_urls.get(selected_repo)

            # If a repository URL is found, start a new thread for git clone
            if repo_url:
                threading.Thread(target=self.perform_git_clone, args=(repo_url, selected_repo), daemon=True).start()
            else:
                messagebox.showerror("Error", "Invalid repository selection.")
        except Exception as e:
            messagebox.showerror("Error", f"Command failed with error: {e}")

    def perform_git_clone(self, repo_url, repo_name):
        try:
            repo_directory = repo_name.lower()

            # Remove the existing directory if it exists
            if os.path.exists(repo_directory):
                shutil.rmtree(repo_directory, ignore_errors=True)

            # Clone the repository
            result = subprocess.check_output(["git", "clone", repo_url], text=True)

            # Display the output in the Text widget
            self.set_text(f"Cloned repository '{repo_name}' successfully:\n{result}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Command failed with error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def set_text(self, message):
        # Clear previous output and set the new message
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, message)

    def setup_git_repos_tab(self):
        git_frame = tk.Frame(self.notebook)

        # Static text above the dropdown menu
        static_text = tk.Label(git_frame, text="Select a repository to clone. If the repository is already cloned, you will get an error.")
        static_text.pack(side=tk.TOP, pady=10)

        # Create a dropdown menu to choose between "UI-Core" and "Backend-Core"
        self.repo_var = tk.StringVar()
        self.repo_var.set("UI-Core")  # Default repository
        repo_menu = tk.OptionMenu(git_frame, self.repo_var, "UI-Core", "Backend-Core")
        repo_menu.pack(side=tk.TOP, pady=10)

        # Create a Text widget to display the output
        self.text_widget = tk.Text(git_frame, height=10, width=60)
        self.text_widget.pack(side=tk.TOP, pady=20)

        # Create a Button to run the git clone command
        clone_button = tk.Button(git_frame, text="Run git clone", command=self.run_clone_command)
        clone_button.pack(side=tk.TOP, pady=20)

        self.notebook.add(git_frame, text="Git Repos")
