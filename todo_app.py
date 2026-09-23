import tkinter as tk
from tkinter import messagebox
import json
import os

FILE_NAME = "tasks.json"


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("550x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f6f8")

        self.tasks = []

        self.create_widgets()
        self.load_tasks()
        self.display_tasks()

    def create_widgets(self):
        # Title
        title = tk.Label(
            self.root,
            text="My To-Do List",
            font=("Arial", 24, "bold"),
            bg="#f4f6f8",
            fg="#2c3e50"
        )
        title.pack(pady=20)

        # Input frame
        input_frame = tk.Frame(self.root, bg="#f4f6f8")
        input_frame.pack(pady=10)

        self.task_entry = tk.Entry(
            input_frame,
            width=35,
            font=("Arial", 13)
        )
        self.task_entry.grid(row=0, column=0, padx=5)

        add_button = tk.Button(
            input_frame,
            text="Add Task",
            command=self.add_task,
            bg="#27ae60",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=10
        )
        add_button.grid(row=0, column=1, padx=5)

        # Task list
        list_frame = tk.Frame(self.root, bg="white", bd=2, relief=tk.GROOVE)
        list_frame.pack(padx=30, pady=15, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_listbox = tk.Listbox(
            list_frame,
            width=55,
            height=18,
            font=("Arial", 12),
            selectmode=tk.SINGLE,
            yscrollcommand=scrollbar.set
        )
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.task_listbox.yview)

        # Buttons
        button_frame = tk.Frame(self.root, bg="#f4f6f8")
        button_frame.pack(pady=15)

        complete_button = tk.Button(
            button_frame,
            text="Complete",
            command=self.complete_task,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12
        )
        complete_button.grid(row=0, column=0, padx=5)

        delete_button = tk.Button(
            button_frame,
            text="Delete",
            command=self.delete_task,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12
        )
        delete_button.grid(row=0, column=1, padx=5)

        clear_button = tk.Button(
            button_frame,
            text="Clear All",
            command=self.clear_tasks,
            bg="#8e44ad",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12
        )
        clear_button.grid(row=0, column=2, padx=5)

        # Enter key support
        self.task_entry.bind("<Return>", lambda event: self.add_task())

    def add_task(self):
        task = self.task_entry.get().strip()

        if not task:
            messagebox.showwarning(
                "Warning",
                "Please enter a task."
            )
            return

        self.tasks.append({
            "task": task,
            "completed": False
        })

        self.task_entry.delete(0, tk.END)
        self.save_tasks()
        self.display_tasks()

    def complete_task(self):
        selected = self.task_listbox.curselection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Please select a task."
            )
            return

        index = selected[0]

        self.tasks[index]["completed"] = True

        self.save_tasks()
        self.display_tasks()

    def delete_task(self):
        selected = self.task_listbox.curselection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Please select a task."
            )
            return

        index = selected[0]

        del self.tasks[index]

        self.save_tasks()
        self.display_tasks()

    def clear_tasks(self):
        if not self.tasks:
            return

        confirm = messagebox.askyesno(
            "Confirm",
            "Are you sure you want to delete all tasks?"
        )

        if confirm:
            self.tasks.clear()
            self.save_tasks()
            self.display_tasks()

    def display_tasks(self):
        self.task_listbox.delete(0, tk.END)

        for task in self.tasks:
            if task["completed"]:
                display_text = "✓ " + task["task"] + " (Completed)"
            else:
                display_text = "○ " + task["task"]

            self.task_listbox.insert(tk.END, display_text)

    def save_tasks(self):
        try:
            with open(FILE_NAME, "w") as file:
                json.dump(self.tasks, file, indent=4)
        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Could not save tasks:\n{error}"
            )

    def load_tasks(self):
        if not os.path.exists(FILE_NAME):
            return

        try:
            with open(FILE_NAME, "r") as file:
                self.tasks = json.load(file)
        except (json.JSONDecodeError, OSError):
            self.tasks = []


# Start application
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
