import tkinter as tk
from tkinter import ttk

def toggle_selection(event):
    # Identify the row under the mouse click
    selected_item = table.identify_row(event.y)
    if selected_item:
        if selected_item in table.selection():
            # Deselect the row if it is already selected
            table.selection_remove(selected_item)
        else:
            # Select the row if it is not already selected
            table.selection_add(selected_item)
    # Prevent default Treeview behavior
    return "break"

# Create the main window
root = tk.Tk()
root.title("Tkinter Table Example")

# Define the columns
columns = ("source_state", "target_state", "interface", "message")

# Create the Treeview widget
table = ttk.Treeview(root, columns=columns, show="headings", selectmode="none")

# Define column headings
column_names = ["Source State", "Target State", "Interface", "Message"]
for col, name in zip(columns, column_names):
    table.heading(col, text=name)
    table.column(col, width=150, anchor="center")

# Add some sample data
data = [
    ("Idle", "Active", "HTTP", "Start Session", 1),
    ("Active", "Complete", "WebSocket", "Send Data", 2),
    ("Complete", "Idle", "REST API", "End Session", 3),
]

for row in data:
    table.insert("", tk.END, values=(row[0], row[1], row[2], row[3]), row[4])

# Bind the click event to the toggle_selection function
table.bind("<Button-1>", toggle_selection)

# Pack the table into the window
table.pack(fill="both", expand=True)

# Start the Tkinter event loop
root.mainloop()
