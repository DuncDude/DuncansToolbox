import tkinter as tk
from tkinter import ttk
from git_operations import GitOperations
from uat_prod_operations import UATProdOperations

def main():
    root = tk.Tk()
    root.title("Duncan's ToolBox")

    notebook = ttk.Notebook(root)

    # Initialize Git Operations
    git_operations = GitOperations(notebook)
    git_operations.setup_git_repos_tab()

    # Initialize UAT/PROD Operations
    uat_prod_operations = UATProdOperations(notebook)
    uat_prod_operations.setup_uat_prod_tab()

    notebook.pack(expand=1, fill="both")

    root.mainloop()

if __name__ == "__main__":
    main()
