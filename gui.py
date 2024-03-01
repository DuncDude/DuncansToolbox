import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import threading
import os
import shutil

def run_clone_command():
    try:
        # Determine the selected repository from the dropdown menu
        selected_repo = repo_var.get()

        # Map the selected repository to the corresponding GitHub URL
        repo_urls = {
            "UI-Core": "https://github.com/DarkFlippers/unleashed-firmware",
            "Backend-Core": "https://github.com/DarkFlippers/Multi_Fuzzer"
        }

        # Get the GitHub URL for the selected repository
        repo_url = repo_urls.get(selected_repo)

        # If a repository URL is found, start a new thread for git clone
        if repo_url:
            set_text(f"Cloning repo {selected_repo}...")
            threading.Thread(target=perform_git_clone, args=(repo_url, selected_repo), daemon=True).start()
        else:
            messagebox.showerror("Error", "Invalid repository selection.")
    except Exception as e:
        messagebox.showerror("Error", f"Command failed with error: {e}")

def run_push_command():
    try:
        # Determine the selected folder from the dropdown menu
        selected_folder = folder_var.get()

        # If a folder is selected, start a new thread for git push
        if selected_folder:
            set_text(f"Pushing changes to folder {selected_folder}...")
            threading.Thread(target=perform_git_push, args=(selected_folder,), daemon=True).start()
        else:
            messagebox.showerror("Error", "Invalid folder selection.")
    except Exception as e:
        messagebox.showerror("Error", f"Command failed with error: {e}")

def set_text(message):
    # Clear previous output and set the new message
    text_widget.delete(1.0, tk.END)
    text_widget.insert(tk.END, message)

def perform_git_clone(repo_url, repo_name):
    try:
        repo_directory = repo_name.lower()

        # Remove the existing directory if it exists
        if os.path.exists(repo_directory):
            shutil.rmtree(repo_directory, ignore_errors=True)

        # Clone the repository
        result = subprocess.check_output(["git", "clone", repo_url], text=True)

        # Display the output in the Text widget
        set_text(f"Cloned repository {repo_name} successfully:\n{result}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Command failed with error: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def perform_git_push(selected_folder):
    try:
        # Push changes to the selected folder
        result = subprocess.check_output(["git", "push", selected_folder], text=True)

        # Display the output in the Text widget
        set_text(f"Pushed changes to folder {selected_folder} successfully:\n{result}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Command failed with error: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def refresh_folder_options(*args):
    # Refresh the dropdown menu options
    working_directory = os.getcwd()
    folder_options = [folder for folder in os.listdir(working_directory) if os.path.isdir(os.path.join(working_directory, folder))]
    
    if folder_options:
        folder_var.set(folder_options[0])
        menu = folder_menu["menu"]
        menu.delete(0, "end")
        for folder in folder_options:
            menu.add_command(label=folder, command=tk._setit(folder_var, folder))
    else:
        folder_var.set("No folders found")

# Create the main window
root = tk.Tk()
root.title("Git Operations")

# Set the size of the main window
root.geometry("600x400")

# Create a notebook (tabbed interface)
notebook = ttk.Notebook(root)

# Create a frame for the "Git Repos" tab
git_repos_frame = tk.Frame(notebook)
notebook.add(git_repos_frame, text="Git Repos")

# Create a dropdown menu to choose between "UI-Core" and "Backend-Core"
repo_var = tk.StringVar()
repo_var.set("UI-Core")  # Default repository
repo_menu = tk.OptionMenu(git_repos_frame, repo_var, "UI-Core", "Backend-Core")
repo_menu.pack(side=tk.TOP, pady=20)

# Create a Text widget to display the output
text_widget = tk.Text(git_repos_frame, height=10, width=60)
text_widget.pack(side=tk.TOP, pady=20)

# Create a Button to run the git clone command
clone_button = tk.Button(git_repos_frame, text="Run git clone", command=run_clone_command)
clone_button.pack(side=tk.TOP, pady=20)

# Create a frame for the "Push to UAT/PROD" tab
push_frame = tk.Frame(notebook)
notebook.add(push_frame, text="Push to UAT/PROD")

# Create a dropdown menu with folder names in the working directory
working_directory = os.getcwd()
folder_var = tk.StringVar()
folder_options = [folder for folder in os.listdir(working_directory) if os.path.isdir(os.path.join(working_directory, folder))]
folder_var.set(folder_options[0] if folder_options else "No folders found")
folder_var.trace_add("write", refresh_folder_options)  # Call refresh_folder_options when folder_var changes
folder_menu = tk.OptionMenu(push_frame, folder_var, *folder_options)
folder_menu.pack(side=tk.TOP, pady=20)

# Create a Text widget to display the output
text_widget_push = tk.Text(push_frame, height=10, width=60)
text_widget_push.pack(side=tk.TOP, pady=20)

# Create a Button to run the git push command
push_button = tk.Button(push_frame, text="Run git push", command=run_push_command)
push_button.pack(side=tk.TOP, pady=20)

# Pack the notebook into the main window
notebook.pack(expand=1, fill="both")

# Start the main event loop
root.mainloop()
