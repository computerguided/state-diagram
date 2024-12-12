import tkinter as tk
from tkinter import ttk

# Create the main application window
root = tk.Tk()
root.title("STADIAE - State Diagram Editor")
root.geometry("1200x800")

# Create the menu bar
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New")
file_menu.add_command(label="Save")
file_menu.add_command(label="Save As")
file_menu.add_command(label="Open")
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About")
menu_bar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menu_bar)

# Create the toolbar
toolbar = tk.Frame(root, bd=1, relief=tk.RAISED)
buttons = ["Save", "Undo", "Redo", "Delete", "Add state", "Add choice-point", "Add transition", "Add interface", "Add message", "Edit"]
for button in buttons:
    btn = tk.Button(toolbar, text=button)
    btn.pack(side=tk.LEFT, padx=2, pady=2)
toolbar.pack(side=tk.TOP, fill=tk.X)

# Create the main frame
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Create the diagram canvas
canvas_frame = tk.Frame(main_frame, width=400, height=400, bg="white")
canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create the right panel with lists and transition table
right_panel = tk.Frame(main_frame)
right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Create lists in a 2x2 grid
lists = ["States", "Choice-points", "Interfaces", "Messages"]
for i, lst in enumerate(lists):
    frame = tk.Frame(right_panel)
    frame.grid(row=i//2, column=i%2, padx=5, pady=5, sticky="nsew")
    label = tk.Label(frame, text=lst)
    label.pack(anchor=tk.W)
    listbox = tk.Listbox(frame, height=5)
    listbox.pack(fill=tk.BOTH, expand=True)

# Configure grid weights for equal distribution
right_panel.grid_rowconfigure(0, weight=1)
right_panel.grid_rowconfigure(1, weight=1)
right_panel.grid_columnconfigure(0, weight=1)
right_panel.grid_columnconfigure(1, weight=1)

# Create the transition table
transition_frame = tk.Frame(right_panel)
transition_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
transition_label = tk.Label(transition_frame, text="Transition Table")
transition_label.pack(anchor=tk.W)
columns = ("Source state", "Interface", "Message", "End state")
tree = ttk.Treeview(transition_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor=tk.W)
tree.pack(fill=tk.BOTH, expand=True)

# Start the application
root.mainloop()
