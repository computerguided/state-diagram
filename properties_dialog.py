import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import Frame, Misc

SINGLE_WORD_INVALID_CHARS = " ±§!@#$%^&()_-+=`~,<.>?/{[}];:\"'\\|\n"

class PropertiesDialog(simpledialog.Dialog):
    def __init__(self, parent, title, fields, labels=None, options=None, field_types=None):
        self.fields = fields
        self.labels = labels or {}
        self.options = options or {}
        self.entries = {}
        self.field_types = field_types or {}
        super().__init__(parent, title)

    def body(self, master: Frame) -> Misc | None:
        row = 0

        # Add labels to the dialog
        for label, value in self.labels.items():
            tk.Label(master, text=label+":").grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
            tk.Label(master, text=value).grid(row=row, column=1, sticky=tk.W, padx=5, pady=2)
            row += 1

        # Add fields to the dialog
        for label, value in self.fields.items():
            tk.Label(master, text=label+":").grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
            field_type = self.field_types.get(label, "text")

            if field_type == "positive_integer":
                entry = tk.Entry(
                    master,
                    validate="key",
                    validatecommand=(master.register(self.validate_positive_integer), '%P')
                )
            elif field_type == "single_word":
                entry = tk.Entry(
                    master,
                    validate="key",
                    validatecommand=(master.register(self.validate_single_word_input), '%P')
                )
            else:
                entry = tk.Entry(master)

            entry.insert(0, value)
            entry.grid(row=row, column=1, sticky=tk.W, padx=5, pady=2)
            self.entries[label] = entry

            if field_type == "positive_integer":
                self.add_increment_decrement_buttons(master, row, label)

            row += 1

        # Add options to the dialog
        for label, (default, options_list) in self.options.items():
            tk.Label(master, text=label+":").grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
            variable = tk.StringVar(master)
            variable.set(default)
            option_menu = tk.OptionMenu(master, variable, *options_list)
            option_menu.grid(row=row, column=1, sticky=tk.W, padx=5, pady=2)
            self.entries[label] = variable
            row += 1

        # Set focus to the first entry field
        if self.fields:
            first_label = next(iter(self.fields))
            return self.entries[first_label]

        return None

    def buttonbox(self):
        box = tk.Frame(self)
        box.pack(side=tk.BOTTOM, fill=tk.X)

        ok_button = tk.Button(
            box,
            text="OK",
            width=10,
            command=self.ok,
            default=tk.ACTIVE
        )
        ok_button.pack(side=tk.LEFT, padx=5, pady=5)

        cancel_button = tk.Button(
            box,
            text="Cancel",
            width=10,
            command=self.cancel
        )
        cancel_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

    def apply(self):
        self.result = {
            label: entry.get()
            for label, entry in self.entries.items()
        }

    def add_increment_decrement_buttons(self, master: Frame, row: int, label: str):
        entry = self.entries[label]
        button_frame = tk.Frame(master)
        button_frame.grid(row=row, column=2, sticky=tk.W, padx=5)

        increment_button = tk.Button(
            button_frame,
            text="▲",
            command=lambda: self.change_value(entry, 1)
        )
        increment_button.pack(side=tk.TOP, fill=tk.X)

        decrement_button = tk.Button(
            button_frame,
            text="▼",
            command=lambda: self.change_value(entry, -1)
        )
        decrement_button.pack(side=tk.TOP, fill=tk.X)

    def change_value(self, entry: tk.Entry, delta: int):
        try:
            current_value = int(entry.get())
        except ValueError:
            current_value = 1
        new_value = max(1, current_value + delta)
        entry.delete(0, tk.END)
        entry.insert(0, str(new_value))

    def validate_positive_integer(self, value_if_allowed: str) -> bool:
        if value_if_allowed.isdigit() and int(value_if_allowed) > 0:
            return True
        elif value_if_allowed == "":
            return True
        else:
            return False

    def validate_single_word_input(self, value_if_allowed: str) -> bool:
        if any(char in SINGLE_WORD_INVALID_CHARS for char in value_if_allowed):
            return False
        return True
