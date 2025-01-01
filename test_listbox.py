import tkinter as tk
from tkinter import messagebox

# Dataset with attached data
items = [
    {"id": 101, "label": "Item 1", "description": "First item"},
    {"id": 102, "label": "Item 2", "description": "Second item"},
    {"id": 105, "label": "Item 3", "description": "Third item"},
    {"id": 108, "label": "Item 4", "description": "Fourth item"},
]

def on_select(event):
    # Get selected indices
    selected_indices = listbox.curselection()
    if selected_indices:
        # Retrieve all selected items
        selected_items = [items[i] for i in selected_indices]

        print("Indices:", selected_indices)

        # Format details for display
        details = "\n".join(
            [f"ID: {item['id']}, Label: {item['label']}, Description: {item['description']}" for item in selected_items]
        )

        messagebox.showinfo("Selected Items", details)

# Create main window
root = tk.Tk()
root.title("Multi-Select Listbox")
root.geometry("400x250")

# Create a listbox with EXTENDED selection mode
listbox = tk.Listbox(root, selectmode=tk.EXTENDED)
listbox.pack(pady=20, fill=tk.BOTH, expand=True)

# Insert labels into the listbox
for item in items:
    listbox.insert(tk.END, item["label"])

# Bind selection event
listbox.bind("<<ListboxSelect>>", on_select)

# Run the application
root.mainloop()
