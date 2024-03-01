import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import subprocess
import threading
import os

class GitOperations:
    def __init__(self, notebook):
        self.notebook = notebook

    def run_clone_command(self):
        try:
            selected_repo = self.repo_var.get()
            threading.Thread(target=self.perform_git_clone, args=(selected_repo,), daemon=True).start()
        except Exception as e:
            messagebox.showerror("Error: Repo may already be in the working directory")
            #messagebox.showerror("Error", f"Command failed with error: {e}")

    def perform_git_clone(self, repo_name):
        try:
            repo_directory = repo_name.lower()

            if os.path.exists(repo_directory):
                messagebox.showinfo("Info", f"Repository '{repo_name}' already exists. Skipping clone.")
            else:
                repo_url = self.repo_urls.get(repo_name)

                if repo_url:
                    self.append_text(f"Cloning repository '{repo_name}'...")
                    subprocess.run(["git", "clone", repo_url], check=True, capture_output=True, text=True)
                    self.append_text(f"Cloned repository '{repo_name}' successfully.")
                else:
                    messagebox.showerror("Error", "Invalid repository selection.")
        except subprocess.CalledProcessError as e:
            self.append_text("Error: Repo may already be in the working directory")
            #self.append_text(f"Command failed with error: {e}")
        except Exception as e:
            self.append_text(f"An unexpected error occurred: {e}")

    def refresh_repo_options(self, *args):
        repo_options = list(self.repo_urls.keys())

        if repo_options:
            self.repo_var.set(repo_options[0])
            menu = self.repo_menu["menu"]
            menu.delete(0, "end")
            for repo in repo_options:
                menu.add_command(label=repo, command=tk._setit(self.repo_var, repo))
        else:
            self.repo_var.set("No repositories found")

    def append_text(self, message):
        current_text = text_widget.get("1.0", tk.END)
        updated_text = current_text + message + "\n"
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, updated_text)

    def setup_git_repos_tab(self):
        git_frame = tk.Frame(self.notebook)

        # Create a frame for dropdown and image
        dropdown_frame = tk.Frame(git_frame)
        dropdown_frame.pack(side=tk.TOP, pady=10)

        # Load and display the image
        image_path = "hackers.png"  # Assuming the image is in the working directory
        image = Image.open(image_path)
        image = image.resize((50, 50), Image.ANTIALIAS)  # Resize the image as needed
        photo = ImageTk.PhotoImage(image)

        image_label = tk.Label(dropdown_frame, image=photo)
        image_label.image = photo  # Keep a reference to the image to prevent it from being garbage collected
        image_label.grid(row=0, column=0, padx=10)

        # Static text above the combobox
        static_label = tk.Label(dropdown_frame, text="Select a repository to clone", font=('Helvetica', 10, 'bold'))
        static_label.grid(row=0, column=1, pady=5)

        # Create a Combobox to choose between repositories
        working_directory = os.getcwd()
        self.repo_var = tk.StringVar()
        self.repo_urls = {
            "UI-Core": "https://github.com/DarkFlippers/unleashed-firmware",
            "Backend-Core": "https://github.com/DarkFlippers/Multi_Fuzzer"
        }
        repo_options = list(self.repo_urls.keys())
        self.repo_var.set(repo_options[0] if repo_options else "No repositories found")

        # Use ttk.Combobox instead of OptionMenu
        repo_combobox = ttk.Combobox(dropdown_frame, textvariable=self.repo_var, values=repo_options, state="readonly")
        repo_combobox.grid(row=1, column=0, columnspan=2, pady=10, padx=10)

        # Create a Text widget to display the output
        global text_widget
        text_widget = tk.Text(git_frame, height=30, width=60)
        text_widget.pack(side=tk.TOP, pady=20)

        # Create a Button to run the git clone command
        clone_button = tk.Button(git_frame, text="Run git clone", command=self.run_clone_command)
        clone_button.pack(side=tk.TOP, pady=20)

        self.notebook.add(git_frame, text="Git Repos")
