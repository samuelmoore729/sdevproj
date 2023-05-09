#This program is designed to allow a user to input their daily tasks and times they wish to complete them by and have them automatically organized and displayed in an orderly fashion with the ability to check things off as they go.

import time
import tkinter as tk
from tkinter import *
import datetime as dt
from tkinter import messagebox
from datetime import datetime

#create the to-do list section of the application
class TodoList:
    
    def __init__(self, master):
        self.master = master
        self.master.title("To-Do List")
        self.master.geometry("400x500")
        self.tasks = []
        self.task_vars = []
        
       
        self.task_label = tk.Label(self.master, text="Enter your 'To-do' tasks:") #Create the 'Enter task' label and entry
        self.task_label.pack()
        self.task_input = tk.Entry(self.master)
        self.task_input.pack()
        
  
        self.time_label = tk.Label(self.master, text="Complete by this time (HH:MM AM/PM):")
        self.time_label.pack()
        self.time_input = tk.Entry(self.master)
        self.time_input.pack()

        self.bottom_frame = tk.Frame(self.master)
        self.bottom_frame.pack(side=tk.BOTTOM, pady=10)

        self.reset_close_frame = tk.Frame(self.master)
        self.reset_close_frame.pack(side=tk.BOTTOM)

        self.add_button = tk.Button(self.master, text="Add Task", command=self.add_task) #Create the add task button
        self.add_button.pack()
       
        self.reset_button = tk.Button(self.reset_close_frame, text="Reset", command=self.reset_tasks)
        self.reset_button.pack(side=tk.RIGHT, padx = 10)

        self.exit_button = tk.Button(self.reset_close_frame, text="Exit", command=self.master.destroy)
        self.exit_button.pack(side=tk.LEFT)

    
       
        self.task_frame = tk.Frame(self.master, bg="light blue")
        self.task_frame.pack(fill=tk.BOTH, expand=True)

      
        self.remaining_label = tk.Label(self.bottom_frame, text=str(len(self.tasks)) + " tasks remaining")
        self.remaining_label.pack()
        
    def add_task(self):
        task = {"task": self.task_input.get(), "time": self.time_input.get()}
        try:
            task_time = datetime.strptime(task["time"], "%I:%M %p")
        except ValueError:
            messagebox.showerror("Invalid time format", "Time format should be in HH:MM AM/PM")
            return

        task["time"] = task_time.strftime("%I:%M %p")
        self.task_input.delete(0, tk.END)
        self.time_input.delete(0, tk.END)

        self.tasks.append(task)

        print(f"Adding task {task}")

        num_remaining = len(self.tasks) - sum([var.get() for var in self.task_vars])
        self.remaining_label.config(text=str(num_remaining) + " tasks remaining")

        self.add_task_checkbox(task)

#Reset button destroys all tasks, resetting the program
    def reset_tasks(self):
        self.tasks = []
        self.task_vars = []
        self.task_input.delete(0, tk.END)
        self.time_input.delete(0, tk.END)
        for widget in self.task_frame.winfo_children():
            widget.destroy()
        self.remaining_label.config(text="0 tasks remaining")

    
    def add_task_checkbox(self, task):
        task_text = task["task"] + " (" + task["time"] + ")"
        task_var = tk.BooleanVar()
        task_var.set(False)
        self.task_vars.append(task_var)

        # Find the position to insert the new task in the task frame
        insert_index = len(self.tasks)
        for i, existing_task in enumerate(self.tasks):
            if existing_task == task:
                insert_index = i
                break

        #Creates the new task checkbox at the correct position in the task frame
        task_checkbutton = tk.Checkbutton(
            self.task_frame, text=task_text, variable=task_var,
            command=lambda task=task, var=task_var: self.check_task(task, var),
            bg="light blue")
        self.task_frame.configure(bg="light blue")
        task_checkbutton.pack(in_=self.task_frame, side=tk.TOP, anchor="center")
        self.task_frame.winfo_children()[insert_index].pack_forget()
        task_checkbutton.pack(in_=self.task_frame, side=tk.TOP, anchor="center")

#Changes the font to overstrike and gray to be more visually appealing when crossing off a completed task
    def check_task(self, task, var):
        
        if var.get():
            task_index = self.tasks.index(task)
            self.task_frame.winfo_children()[task_index].config(fg="gray", font=("Arial", 10, "overstrike"))

        
        else:
            task_index = self.tasks.index(task)
            self.task_frame.winfo_children()[task_index].config(fg="black", font=("Arial", 10, "normal"))

        
        num_remaining = sum([not var.get() for var in self.task_vars])
        self.remaining_label.config(text=str(num_remaining) + " tasks remaining")

class Notes:
    def __init__(self, master):
        self.master = master
        self.master.title("Notes")
        self.master.geometry("400x700")
        self.notes = ""

        self.notelogo = PhotoImage(name="Notebook clipart", file="notebook.png").subsample(10)
        
        # Create a Label widget and set its image option to the photo image
        notelogo = tk.Label(self.master, image=self.notelogo, bd=5, bg="white")
        notelogo.pack()

        self.notes_label = tk.Label(self.master, text="Enter your notes:")
        self.notes_label.pack()

        self.notes_input = tk.Text(self.master, height=20, width=50)
        self.notes_input.pack()

    

        self.save_frame =tk.Frame(self.master, bg="white")
        self.save_frame.pack(fill=tk.BOTH, expand=True)

        self.save_button = tk.Button(self.save_frame, text="Save", command=self.save_notes)
        self.save_button.pack(side=tk.BOTTOM)

        self.close_button = tk.Button(self.master, text="Close", command=self.master.destroy)
        self.close_button.pack(side=tk.BOTTOM)

    def save_notes(self):
        self.notes = self.notes_input.get("1.0", tk.END)
        with open("notes.txt", "w") as f:
            f.write(self.notes)



class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x400")
        self.root.configure(bg="#ADD8E6") # Set background color to light blue

        title_label = tk.Label(self.root, text="ToDoList by Sam Moore", font=("Arial", 20), bg="#ADD8E6")
        title_label.pack(pady=10)

        self.logo_image = PhotoImage(name="Calendar Photo", file="calendar.png").subsample(4)
        
        # Create a Label widget and set its image option to the photo image
        logo_label = tk.Label(self.root, image=self.logo_image, bd=5, bg="light blue")
        logo_label.pack()

        subtitle_label = tk.Label(self.root, text="Which part of the program would you like to access?", font=("Arial", 12), bg="#ADD8E6")
        subtitle_label.pack()

        self.todo_frame = tk.Frame(self.root, bg="light blue")
        self.todo_frame.pack(fill=tk.BOTH, expand=True)

        self.notes_frame = tk.Frame(self.root, bg="light blue")
        self.notes_frame.pack(fill=tk.BOTH, expand=True)

        self.exit_frame = tk.Frame(self.root, bg="light blue")
        self.exit_frame.pack(fill=tk.BOTH, expand=True)

        self.todo_button = tk.Button(self.todo_frame, text="To-Do List", command=self.open_todo_list,)
        self.todo_button.pack(pady= 15)

        self.notes_button = tk.Button(self.notes_frame, text="Notes", command=self.open_notes)
        self.notes_button.pack(side=TOP, pady= 10)

        self.exit_button = tk.Button(self.exit_frame, text="Exit", command=self.root.quit)
        self.exit_button.pack()


    def open_todo_list(self):
        todo_window = tk.Toplevel(self.root)
        todo_list = TodoList(todo_window)

    def open_notes(self):
        notes_window = tk.Toplevel(self.root)
        notes = Notes(notes_window)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MainWindow()
    app.run()
