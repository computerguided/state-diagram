import tkinter as tk
from tkinter import simpledialog, messagebox
from properties_dialog import PropertiesDialog

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Main Window")
        self.geometry("300x200")

        tk.Button(self, text="State Properties", command=self.open_state_properties).pack(pady=5)
        tk.Button(self, text="Choice-point Properties", command=self.open_choice_point_properties).pack(pady=5)
        tk.Button(self, text="Interface Properties", command=self.open_interface_properties).pack(pady=5)
        tk.Button(self, text="Message Properties", command=self.open_message_properties).pack(pady=5)
        tk.Button(self, text="Transition Properties", command=self.open_transition_properties).pack(pady=5)
        tk.Button(self, text="Example Properties", command=self.open_example_properties).pack(pady=5)

    def open_state_properties(self):
        fields = {"Name": "", "Display name": ""}
        field_types = {"Name": "single_word", "Display name": "text"}
        dialog = PropertiesDialog(self, "State Properties", fields, field_types=field_types)
        if dialog.result:
            messagebox.showinfo("State Properties", f"Name: {dialog.result['Name']}\nDisplay name: {dialog.result['Display name']}")

    def open_choice_point_properties(self):
        fields = {"Name": "", "Question": ""}
        field_types = {"Name": "single_word", "Question": "text"}
        dialog = PropertiesDialog(self, "Choice-point Properties", fields, field_types=field_types)
        if dialog.result:
            messagebox.showinfo("Choice-point Properties", f"Name: {dialog.result['Name:']}\nQuestion: {dialog.result['Question:']}")

    def open_interface_properties(self):
        fields = {"Name": ""}
        field_types = {"Name": "single_word"}
        dialog = PropertiesDialog(self, "Interface Properties", fields, field_types=field_types)
        if dialog.result:
            messagebox.showinfo("Interface Properties", f"Name: {dialog.result['Name:']}")

    def open_message_properties(self):
        labels = {"Interface:": "Interface Name"}
        fields = {"Name": ""}
        field_types = {"Name": "single_word"}
        dialog = PropertiesDialog(self, "Message Properties", fields, labels, field_types=field_types)
        if dialog.result:
            messagebox.showinfo("Message Properties", f"Interface: {labels['Interface:']}\nName: {dialog.result['Name:']}")

    def open_transition_properties(self):
        labels = {
            "Source state": "Source State",
            "Interface": "Interface Name",
            "Message": "Message Name",
            "Target state": "Target State"
        }
        fields = {
            "Connector length": 1
        }
        options = {
            "Connector type": ("Up", ["Left", "Right", "Up", "Down"])
        }
        field_types = {"Connector length": "positive_integer"}
        dialog = PropertiesDialog(self, "Transition Properties", fields, labels, options, field_types=field_types)
        if dialog.result:
            messagebox.showinfo("Transition Properties", "\n".join(f"{k} {v}" for k, v in {**labels, **dialog.result}.items()))

    def open_example_properties(self):
        labels = {
            "Example Label": "This is an example label",
            "Second Example Label": "This is another example label"
        }
        fields = {
            "Positive Integer": "1",
            "Single Word": "",
            "Text": "Default text"
        }
        options = {
            "Example Option": ("Option1", ["Option1", "Option2", "Option3"])
        }
        field_types = {
            "Positive Integer": "positive_integer",
            "Single Word": "single_word",
            "Text": "text"
        }
        dialog = PropertiesDialog(self, "Example Properties", fields, labels, options, field_types)
        if dialog.result:
            messagebox.showinfo("Example Properties", "\n".join(f"{k}: {v}" for k, v in dialog.result.items()))

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
