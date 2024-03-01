import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import subprocess
import threading
import os

class UATProdOperations:
    def __init__(self, notebook):
        self.notebook = notebook

    def run_push_command(self, target):
        try:
            selected_folder = self.folder_var.get()
            self.append_text(f"*********** Starting: {selected_folder}*********** ")
            selected_option = self.push_option_var.get()  # Get the selected radio button option

            if selected_folder:
                threading.Thread(target=self.perform_git_push, args=(selected_folder, selected_option), daemon=True).start()
            else:
                messagebox.showerror("Error", "Invalid folder selection.")
        except Exception as e:
            messagebox.showerror("Error", f"Command failed with error: {e}")

    def perform_git_push(self, selected_folder, selected_option):
        try:
            self.append_text(f"Changing directory to {selected_folder}...")
            os.chdir(selected_folder)  # Change to the selected directory

            self.append_text("Checking out 'uat' branch...")
            try:
                subprocess.run(["git", "checkout", "uat"], check=True, capture_output=True, text=True)
            except:
                self.append_text("Branch 'uat' not found, creating...")
                subprocess.run(["git", "checkout", "-b", "uat"], check=True, capture_output=True, text=True)

            try:
                self.append_text("Merging 'master' into 'uat'...")
                subprocess.run(["git", "merge", "master"], check=True, capture_output=True, text=True)

                push_command = ["git", "push", "origin", "uat"]

                if selected_option == "Force":
                    push_command.append("-f")
                elif selected_option == "Fast Forward":
                    push_command.append("-ff")

                self.append_text(f"Pushing changes to 'uat' with option: {selected_option}...")
                subprocess.run(push_command, check=True, capture_output=True, text=True)

                self.append_text(f"Pushed changes to 'uat' successfully with option: {selected_option}.")
            except subprocess.CalledProcessError as e:
                self.append_text(f"Command failed with error: {e}")
        except Exception as e:
            self.append_text(f"Something went terribly wrong: {e}")
        finally:
            os.chdir(os.path.dirname(os.path.realpath(__file__)))

    def refresh_folder_options(self, *args):
        # Refresh the dropdown menu options excluding "__pycache__" and ".git"
        working_directory = os.getcwd()
        folder_options = [folder for folder in os.listdir(working_directory) if os.path.isdir(os.path.join(working_directory, folder)) and folder not in ["__pycache__", ".git"]]

        if folder_options:
            self.folder_var.set(folder_options[0])
            menu = self.folder_menu["menu"]
            menu.delete(0, "end")
            for folder in folder_options:
                menu.add_command(label=folder, command=tk._setit(self.folder_var, folder))
        else:
            self.folder_var.set("No folders found")

    def append_text(self, message):
        # Append the new message to the existing text
        current_text = text_widget_push.get("1.0", tk.END)
        updated_text = current_text + message + "\n"
        text_widget_push.delete("1.0", tk.END)
        text_widget_push.insert(tk.END, updated_text)

        # Auto-scroll to the bottom
        text_widget_push.yview(tk.END)


    def setup_uat_prod_tab(self):
        push_frame = tk.Frame(self.notebook)

        # Create a frame for dropdown and image
        dropdown_frame = tk.Frame(push_frame)
        dropdown_frame.pack(side=tk.TOP, pady=10)

        # Load and display the image
        image_path = "hackers.png"  # Assuming the image is in the working directory
        image = Image.open(image_path)
        image = image.resize((50, 50), Image.ANTIALIAS)  # Resize the image as needed
        photo = ImageTk.PhotoImage(image)

        image_label = tk.Label(dropdown_frame, image=photo)
        image_label.image = photo  # Keep a reference to the image to prevent it from being garbage collected
        image_label.grid(row=0, column=0, padx=10)

        # Static text above the dropdown menu
        static_label = tk.Label(dropdown_frame, text="Select repo you wish to push to UAT/Prod", font=('Helvetica', 10, 'bold'))
        static_label.grid(row=0, column=1, pady=5)

        working_directory = os.getcwd()
        folder_options = [folder for folder in os.listdir(working_directory) if os.path.isdir(os.path.join(working_directory, folder)) and folder not in ["__pycache__", ".git"]]
        self.folder_var = tk.StringVar(value=folder_options[0] if folder_options else "No folders found")
        
        # Use Combobox instead of OptionMenu
        self.folder_menu = ttk.Combobox(dropdown_frame, textvariable=self.folder_var, values=folder_options, state="readonly")
        self.folder_menu.grid(row=1, column=0, columnspan=2, pady=10, padx=10)

        # Create a Text widget to display the output
        global text_widget_push
        text_widget_push = tk.Text(push_frame, height=30, width=60)
        text_widget_push.pack(side=tk.TOP, pady=20)

        # Create a Scrollbar
        scrollbar = tk.Scrollbar(push_frame, command=text_widget_push.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Set the Text widget to use the Scrollbar
        text_widget_push.config(yscrollcommand=scrollbar.set)

        # Create a frame for radio buttons
        radio_frame = tk.Frame(push_frame)
        radio_frame.pack(side=tk.TOP, pady=10)

        # Radio buttons
        self.push_option_var = tk.StringVar()
        force_button = tk.Radiobutton(radio_frame, text="Force", variable=self.push_option_var, value="Force")
        force_button.grid(row=0, column=0, padx=10)
        fast_forward_button = tk.Radiobutton(radio_frame, text="Fast Forward (not recommend)", variable=self.push_option_var, value="Fast Forward")
        fast_forward_button.grid(row=0, column=1, padx=10)

        # Create a frame for the buttons
        button_frame = tk.Frame(push_frame)
        button_frame.pack(side=tk.TOP, pady=20)

        # Create a Button to run the git push command for UAT
        push_uat_button = tk.Button(button_frame, text="Push to UAT", command=lambda: self.run_push_command("uat"))
        push_uat_button.pack(side=tk.LEFT, padx=10)

        # Create a Button to run the git push command for Prod
        push_prod_button = tk.Button(button_frame, text="Push to Prod", command=lambda: self.run_push_command("prod"))
        push_prod_button.pack(side=tk.LEFT, padx=10)

    # ... (rest of the code)
    
        self.notebook.add(push_frame, text="Push to UAT/PROD")


        # ... (rest of the code)
        
        self.notebook.add(push_frame, text="Push to UAT/PROD")
