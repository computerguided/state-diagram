# Application

_The `Application` class is the main class of the application. It is responsible for the GUI and the logic of the application._

## Dependencies

The `Application` class depends on the following classes:

- `PlantUMLManager`: to hold the diagram and all the administration of the elements and transitions in the diagram.
- `Element`: to hold the elements of the diagram.
- `ImageTk`: to hold the image of the diagram in the diagram canvas.

```python
from plantuml_manager import PlantUMLManager
from element import Element, ElementType
from PIL import ImageTk
```

## Constants

To hold the title and the window size, the following constants are defined:

```python
TITLE = "STADIAE - State Diagram Editor"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
```

The main menu items and their subitems are predefined in the `MENU_ITEMS` dictionary.

```python
MENU_ITEMS = {
    "File": ["New", "Save", "Save As", "Open", "Exit"],
    "Components": ["Change name", "Change transition font size", "Change state font size"],
    "Help": ["About"]
}
```

The toolbar buttons are stored in the `TOOLBAR_BUTTONS` list.

```python
TOOLBAR_BUTTONS = ["Save", "Undo", "Redo", "Delete", "Add state", "Add choice-point", "Add transition", "Add interface", "Add message", "Edit"]
```

The columns for the transition table are stored in the `COLUMNS` variable.

```python
COLUMNS = ("source_state", "target_state", "interface", "message")
```

## Application

The `Application` class is the main class of the application. It is responsible for the GUI and the logic of the application.

To hold the GUI elements, the class has the following attributes:

| Attribute | Type | Description |
| --- | --- | --- |
| `root` | `tk.Tk` | The root window. |
| `main_content` | `ttk.Frame` | The main content area holding all the GUI elements. |
| `toolbar` | `ttk.Frame` | The toolbar holding the toolbar buttons. |
| `diagram_canvas` | `ttk.Frame` | The diagram canvas holding the diagram. |
| `right_panel` | `ttk.Frame` | The right panel holding the listboxes for the states, choice-points, interfaces and messages and the transition table. |

Inside the `right_panel` frame, the following GUI elements are created:

| Attribute | Type | Description |
| --- | --- | --- |
| `elements_listbox` | `dict[ElementType, tk.Listbox]` | A dictionary of `tk.Listbox` objects holding the elements of a specific type. |
| `transitions_table` | `ttk.Treeview` | The transitions table holding the transitions with the columns `Source state`, `Target state`, `Interface` and `Message`. |

To stored the administration of the diagram, the following attributes are used:

| Attribute | Type | Description |
| --- | --- | --- |
| `plantuml_manager` | `PlantUMLManager` | Holding the diagram and all the administration of the elements and transitions in the diagram. |
| `diagram_canvas_image` | `ImageTk.PhotoImage` | Representing the current image in the diagram canvas in order to keep a reference to the current image in the diagram canvas. |

To be able to associate the index of a listbox item with the corresponding element in the `PlantUMLManager` object the following dictionary is used:

| Attribute | Type | Description |
| --- | --- | --- |
| `elements` | `dict[ElementType, list[Element]]` | A dictionary holding a lexicographically ordered list of elements of a specific type. |

## Methods

The `Application` class has the following methods to create the GUI elements:

- [`create_main_window()`](#create-the-main-application-window): creates the main window.
- [`create_menu_bar()`](#create-the-menu-bar): creates the menu bar.
- [`create_frames_and_panels()`](#create-frames-and-panels): creates the frames and panels.
- [`create_toolbar()`](#create-toolbar): creates the toolbar.
- [`create_listboxes()`](#create-the-listboxes): creates the listboxes.
- [`create_listbox()`](#create-listbox): creates a listbox in a specific frame.
- [`create_transition_table()`](#create-the-transition-table): creates the transition table.

To fill the listboxes and the transition table with data, the following methods are used:
- [`fill_states_listbox()`](#fill-states-listbox): fills the states listbox.
- [`fill_choice_points_listbox()`](#fill-choice-points-listbox): fills the choice points listbox.
- [`fill_interfaces_listbox()`](#fill-interfaces-listbox): fills the interfaces listbox.
- [`fill_messages_listbox()`](#fill-messages-listbox): fills the messages listbox.
- [`fill_transitions_table()`](#fill-transitions-table): fills the transition table.

All the listboxes are filled using the generic [`fill_listbox_with_elements()`](#fill-listbox-with-elements) method:
- [`fill_listbox_with_elements()`](#fill-listbox-with-elements): generic method to fill a listbox with elements.

For handling the click events, the following methods are used:
- [`on_menu_item_click()`](#menu-item-click-handler): handles the click event for the menu items.
- [`on_toolbar_button_click()`](#toolbar-button-click-handler): handles the click event for the toolbar buttons.
- [`on_listbox_item_click()`](#listbox-item-click-handler): handles the click event for the listbox items.
- [`on_transition_table_item_click()`](#transition-table-item-click-handler): handles the click event for the transition table items.
- [`on_diagram_canvas_item_click()`](#diagram-canvas-item-click-handler): handles the click event for the diagram canvas items.
- [`deselect_all_elements()`](#deselect-all-elements): deselects all elements.

To show a diagram in the diagram canvas, the following method is used:
- [`show_diagram()`](#show-diagram): shows a diagram in the diagram canvas.

To add an element to the diagram, the following methods are used:
- [`add_element()`](#add-element): adds an element to the diagram.
- [`add_state()`](#add-state): adds a state to the diagram.
- [`add_choice_point()`](#add-choice-point): adds a choice-point to the diagram.
- [`add_interface()`](#add-interface): adds an interface to the diagram.
- [`add_message()`](#add-message): adds a message to the diagram.
- [`add_transition()`](#add-transition): adds a transition to the diagram.

To delete an element from the diagram, the following methods are used:
- [`delete_element()`](#delete-element): deletes an element from the diagram.
- [`delete_transition()`](#delete-transition): deletes a transition from the diagram.

## Selecting elements

The following describes the behavior of the application when an element is selected.

Firstly, when an element is clicked in the diagram, it should be handled as if the corresponding element was clicked in the listbox as well.

A special case is when a transition is clicked in the diagram canvas. In this case, _all_ the transitions in the transition table with the same source and target states are considered to be 'clicked'.

When a state or choice-point is clicked in a listbox and the selection is changed, the selection is also changed in the diagram canvas.

When a row is clicked in the transition table, the transitions are only selected in the diagram canvas if _all_ the transitions with the same source and target states are selected.

Note that the listboxes and the transition table are filled with data from the `PlantUMLManager` object and the `identifier` of the elements is used to set the `id` attribute of the elements in the listboxes and the transition table.














## Create the main application window

To create the main application window, the `create_main_window()` method is called.

```python
def create_main_window(self, title: str, width: int, height: int) -> tk.Tk:
```

Using the supplied title, width and height, the method creates a `tk.Tk` object and returns it.

```python
root = tk.Tk()
root.title(TITLE)
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
return root
```

## Create the menu bar

To create the menu bar, the `create_menu_bar()` method is called.

```python
def create_menu_bar(self, root: tk.Tk) you Ok Hi Ok Ok Hi I Ok Hi Hi Hi :
```

First, the method creates the menu bar which is a `tk.Menu` object.

```python
menu_bar = tk.Menu(root)
```

It then iterates over the `MENU_ITEMS` dictionary and adds the items to the menu bar.

```python
for category, items in MENU_ITEMS.items():
```

In the inner loop, the method creates a `tk.Menu` object.

```python
menu = tk.Menu(menu_bar, tearoff=0)
```

It then adds the menu to the menu bar.

```python
menu_bar.add_cascade(label=category, menu=menu)
```

Finally, the method iterates over the items and adds them to the menu.

```python
for item in items:
    menu.add_command(label=item, command=lambda item=item: self.on_menu_item_click(item))
```

After all the items are added, the root window is configured to use the menu bar.

```python
root.config(menu=menu_bar)
```

## Create frames and panels

To create the frames and panels, the `create_frames_and_panels()` method is called.

```python
def create_frames_and_panels(self):
```

First the method creates the main content frame. The frame is added to the root window and it is configured to fill the root window and expand when the window is resized.

```python
self.main_content = ttk.Frame(self.root)
self.main_content.pack(fill=tk.BOTH, expand=True)
```

Then the frame for the canvas is created on the left side of the main content frame.

```python
self.canvas_frame = ttk.Frame(self.main_content, width=400, height=400, bg="white")
self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
```

The frame for the right panel is created on the right side of the main content frame.

```python
self.right_panel = ttk.Frame(self.main_content)
self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
```

## Create the listboxes

To create the listboxes, the `create_listboxes()` method is called.

```python
def create_listboxes(self):
```

The listboxes are created in a 2x2 grid.

```python
self.elements_listbox[ElementType.STATE] = self.create_listbox("States", 0, 0)
self.elements_listbox[ElementType.CHOICE_POINT] = self.create_listbox("Choice points", 0, 1)
self.elements_listbox[ElementType.INTERFACE] = self.create_listbox("Interfaces", 1, 0)
self.elements_listbox[ElementType.MESSAGE] = self.create_listbox("Messages", 1, 1)
```

## Create listbox

To create a listbox in a specific frame, the `create_listbox()` method is called, which creates a new `tk.Listbox` object in a grid.

```python
def create_listbox(self, name : str, row : int, column : int) -> tk.Listbox:
```

The method creates a new `tk.Listbox` object and adds it to the grid.

The first step is to create a new Frame widget. It is being created as a child of `self.right_panel`, meaning it will be placed inside the `right_panel` frame of the application.

```python
frame = tk.Frame(self.right_panel)
```

The next step is to place the frame in a grid layout within its parent widget (self.right_panel).

```python
frame.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")
```

Parameters:
- `row`: Determines the row position of the frame in the grid.
- `column`: Determines the column position of the frame in the grid.
- `padx=5, pady=5`: Adds padding of 5 pixels around the frame, both horizontally (`padx`) and vertically (`pady`).
- `sticky="nsew"`: Ensures that the frame will expand to fill the available space in all directions (north, south, east, west) within its grid cell.

In the created frame, a label must be added that will display the name of the listbox. The label is added to the frame using the `pack()` method, which is a layout manager for the frame. The `anchor=tk.W` parameter ensures that the label is aligned to the left side of the frame.

```python
label = tk.Label(frame, text=name)
label.pack(anchor=tk.W)
```

Finally, the method creates a new `tk.Listbox` object and adds it to the frame. The height of the listbox is set to 5 and the select mode is set to multiple. Then the `pack()` method is called to add the listbox to the frame with the `fill=tk.BOTH, expand=True` parameters to ensure that the listbox will expand to fill the available space in both directions.

```python
listbox = tk.Listbox(frame, height=5, selectmode=tk.MULTIPLE)
listbox.pack(fill=tk.BOTH, expand=True)
```

Finally, a handler [`on_listbox_item_click()`](#listbox-item-click-handler) is set for the left mouse button click event ("<Button-1>") using the `bind()` method.

```python
listbox.bind("<Button-1>", lambda event, listbox=listbox: self.on_listbox_item_click(listbox))
```

The method returns the created `tk.Listbox` object.

```python
return listbox
```

## Create the transition table

To create the transition table, the `create_transition_table()` method is called.

```python
def create_transition_table(self) -> ttk.Treeview:
```

First the method creates a new `ttk.Treeview` object. Because we want to be able to select multiple rows, the `selectmode="none"` parameter is passed to the `ttk.Treeview` constructor.

```python
table = ttk.Treeview(self.right_panel, columns=columns, show="headings", selectmode="none")
```

The columns are defined in the `COLUMNS` variable and the method iterates over the columns and defines the column headings. The column headings are defined by replacing the underscores in the column name with spaces and converting the first letter of each word to uppercase, e.g. "source_state" becomes "Source State".

```python
for col in COLUMNS:
    table.heading(col, text=col.replace("_", " ").upper())
    table.column(col, width=150, anchor="center")
```

The method packs the table into the right panel.

```python
table.pack(fill="both", expand=True)
```

A handler [`on_transition_table_item_click()`](#transition-table-item-click-handler) is set for the left mouse button click event ("<Button-1>") using the `bind()` method. THe handler doesn't have any parameters because there is only one transition table and it is always the same.

```python
table.bind("<Button-1>", lambda event: self.on_transition_table_item_click())
```

The method returns the created `ttk.Treeview` object.

```python
return table
```

## Fill states listbox

To fill the states listbox, the `fill_states_listbox()` method is called.

```python
def fill_states_listbox(self):
```

The first step is to retrieve the states from the `PlantUMLManager` object and place them in the appropriate `listbox_item_to_element` list of tuples, where the first element is the `name` or - if not empty - their `display_name` attribute and the second element is the state object itself.

```python
listbox_item_to_element[ElementType.STATE] = [
    (state.display_name if state.display_name else state.name, state)
    for state in self.plantuml_manager.get_elements_by_type(ElementType.STATE)
]
``` 

The second step is to call the generic [`fill_listbox_with_elements()`](#fill-listbox-with-elements) method with the type set to `ElementType.STATE`.

```python
self.fill_listbox_with_elements(ElementType.STATE)
```

In this way the index of the listbox item is the same as the index of the state in the `listbox_item_to_element[ElementType.STATE]` list.

## Fill choice-points listbox

To fill the choice-points listbox, the `fill_choice_points_listbox()` method is called.

```python
def fill_choice_points_listbox(self):
```

The first step is to retrieve the choice-points from the `PlantUMLManager` object and place them in the appropriate `listbox_item_to_element` list of tuples, where the first element is the `question` attribute and the second element is the choice-point object itself.

```python
listbox_item_to_element[ElementType.CHOICE_POINT] = [
    (choice_point.question, choice_point)
    for choice_point in self.plantuml_manager.get_elements_by_type(ElementType.CHOICE_POINT)
]
```

Then the generic [`fill_listbox_with_elements()`](#fill-listbox-with-elements) method is called with the type set to `ElementType.CHOICE_POINT`.

```python
self.fill_listbox_with_elements(ElementType.CHOICE_POINT)
```

In this way the index of the listbox item is the same as the index of the choice-point in the `listbox_item_to_element[ElementType.CHOICE_POINT]` list.

## Fill interfaces listbox

To fill the interfaces listbox, the `fill_interfaces_listbox()` method is called.

```python
def fill_interfaces_listbox(self):
```

The first step is to retrieve the interfaces from the `PlantUMLManager` object and place them in the appropriate `listbox_item_to_element` list of tuples, where the first element is the `name` attribute and the second element is the interface object itself.

```python
listbox_item_to_element[ElementType.INTERFACE] = [
    (interface.name, interface)
    for interface in self.plantuml_manager.get_elements_by_type(ElementType.INTERFACE)
]
```

Then the generic [`fill_listbox_with_elements()`](#fill-listbox-with-elements) method is called with the `listbox_item_to_element[ElementType.INTERFACE]` list and the `self.interfaces_listbox` listbox.

```python
self.fill_listbox_with_elements(ElementType.INTERFACE)
```

In this way the index of the listbox item is the same as the index of the interface in the `listbox_item_to_element[ElementType.INTERFACE]` list.

## Fill messages listbox

To fill the messages listbox, the `fill_messages_listbox()` method is called.

```python
def fill_messages_listbox(self):
```

The first step is to retrieve all the messages from the `PlantUMLManager` object for which the `interface` attribute is the same as the currently selected interface and place them in the `messages_listbox_item_to_element` list of tuples, where the first element is the `name` attribute and the second element is the message object itself.

```python
listbox_item_to_element[ElementType.MESSAGE] = [
    (message.name, message)
    for message in self.plantuml_manager.get_elements_by_type(ElementType.MESSAGE)
    if message.interface == self.interfaces_listbox.curselection()
]
```

Then the generic [`fill_listbox_with_elements()`](#fill-listbox-with-elements) method is called with the type set to `ElementType.MESSAGE`.

```python
self.fill_listbox_with_elements(ElementType.MESSAGE)
```

In this way the index of the listbox item is the same as the index of the message in the `listbox_item_to_element[ElementType.MESSAGE]` list.

## Fill listbox with elements

To fill a listbox with elements, the generic `fill_listbox_with_elements()` method is called.

```python
def fill_listbox_with_elements(self, element_type: ElementType):
```

The method performs the following steps:

1. Sort the elements by their first attribute, which is a string.
2. Clear the listbox.
3. Iterate over the elements and add them to the listbox.

These steps are implemented as described below.

The first step is to sort the elements by their first attribute, which is a string.

```python
listbox_item_to_element[element_type].sort(key=lambda x: x[0])
```

The second step is to clear the listbox.

```python
self.elements_listbox[element_type].delete(0, tk.END)
```

The third step is to iterate over the elements and add them to the listbox.

```python
for element in listbox_item_to_element[element_type]:
    self.elements_listbox[element_type].insert(tk.END, element[0])
```

In this way the index of the listbox item is the same as the index of the element in the `elements` list.

## Fill transitions table

To fill the transitions table, the `fill_transitions_table()` method is called.

```python
def fill_transitions_table(self):
```

The first step is to retrieve the transitions from the `PlantUMLManager` object and place them in the appropriate `elements` list. This is done by calling the [`get_elements_by_type()`](#get-elements-by-type) method with the type set to `ElementType.TRANSITION`.

```python
elements[ElementType.TRANSITION] = self.plantuml_manager.get_elements_by_type(ElementType.TRANSITION)
```

However, there is only one transition per source state and target state pair, which contains a list of messages. Therefore, the method must split the transitions into separate transitions for each message because in the transition table each message must be shown as a separate row.

```python
elements[ElementType.TRANSITION] = [transition for transition in elements[ElementType.TRANSITION] for message in transition.messages]
```

The second step is to order the transitions by their `source_state`, `target_state`, `interface` and `message` attributes.

```python
elements[ElementType.TRANSITION].sort(key=lambda transition: (transition.source_state, transition.target_state, transition.interface, transition.message))
```

The third step is to clear the table.

```python
self.transitions_table.delete(*self.transitions_table.get_children())
```

The fourth step is to iterate over the transitions and add them to the table.

```python
for transition in elements[ElementType.TRANSITION]:
    self.transitions_table.insert("", tk.END, values=(transition.source_state, transition.target_state, transition.interface, transition.message))
```

In this way the index of the table row is the same as the index of the transition in the `transitions` list.

## Create the toolbar

To create the toolbar, the `create_toolbar()` method is called.

```python
def create_toolbar(self):
```

The method creates a new `tk.Frame` object and adds it to the root window.

```python
toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
```

The method then iterates over the `buttons` list.

```python
for button_name in TOOLBAR_BUTTONS:
```

For each button, a new `tk.Button` object is created and added to the toolbar frame. The `side=tk.LEFT` parameter ensures that the button is added to the left side of the frame. The `padx=2, pady=2` parameters add padding of 2 pixels around the button.

```python
button = tk.Button(toolbar, text=button_name)
button.pack(side=tk.LEFT, padx=2, pady=2)
```

Then, the method sets a handler `on_toolbar_button_click()` for the left mouse button click event ("<Button-1>") using the `bind()` method.

```python
button.bind("<Button-1>", lambda event, button_name=button_name: self.on_toolbar_button_click(button_name))
```

In this call the `lambda` keyword is used to create an anonymous function that takes the `event` parameter and the `button` parameter and passes them to the `on_toolbar_button_click()` method.

When all buttons are created, the toolbar's `pack()` method is called to add the toolbar to the root window.

```python
toolbar.pack(side=tk.TOP, fill=tk.X)
```

The method returns the created `tk.Frame` object.

```python
return toolbar
```

## Toolbar button click handler

To handle the click event for a toolbar button, the `on_toolbar_button_click()` method is called.

```python
def on_toolbar_button_click(self, button_name: str):
```

The `button_name` parameter is the text of the button that was clicked and can be used to determine which action to perform.

```python
if button_name == "Save":
    self.save_diagram()
elif button_name == "Undo":
    self.undo_last_action()
elif button_name == "Redo":
    self.redo_last_action()
elif button_name == "Delete":
    self.delete_selected_item()
elif button_name == "Add state":
    self.add_state()
elif button_name == "Add choice-point":
    self.add_choice_point()
elif button_name == "Add transition":
    self.add_transition()
elif button_name == "Add interface":
    self.add_interface()
elif button_name == "Add message":
    self.add_message()
elif button_name == "Edit":
    self.edit_selected_item()
```

## Listbox item click handler

To handle the click event for a listbox item, the `on_listbox_item_click()` method is called.

```python
def on_listbox_item_click(self, listbox: tk.Listbox):
```

The `listbox` parameter is the listbox that was clicked.

The first step is to retrieve the set of identifiers that are currently selected in the listbox.

```python
selected_identifiers = listbox.curselection()
```

The method then checks which listbox was clicked and sets the `element_type` variable.

```python
if listbox == self.states_listbox:
    element_type = ElementType.STATE
elif listbox == self.choice_points_listbox:
    element_type = ElementType.CHOICE_POINT
elif listbox == self.interfaces_listbox:
    element_type = ElementType.INTERFACE
elif listbox == self.messages_listbox:
    element_type = ElementType.MESSAGE
```

Using the appropriate `elements` variable, the method can retrieve the `identifier` attribute of the corresponding elements, which is the second element of the tuple.

```python
selected_identifiers = [elements[element_type][i][1].identifier for i in selected_identifiers]
```

Now that the `element_type` variable is set, in order to keep consistency, the method first deselects all the elements of the same type in the `PlantUMLManager` object.

```python
self.plantuml_manager.deselect_elements(element_type)
```

Then the method selects the elements in the `PlantUMLManager` object.

```python
self.plantuml_manager.select_identifiers(selected_identifiers)
```

At this point the `plantuml_manager` object knows which elements are selected and it needs to be notified that the selection has changed when the clicked listbox is a state or choice-point listbox.

```python
if element_type == ElementType.STATE or element_type == ElementType.CHOICE_POINT:
    self.plantuml_manager.notify_selection_change()
```

This will trigger the `PlantUMLManager` object to render the diagram indicating the selected elements.

When the clicked listbox is an interface listbox, the messages listbox is updated because only those messages that are associated with the selected interface are shown. This is done by calling the `fill_messages_listbox()` method.

```python
elif element_type == ElementType.INTERFACE:
    self.fill_messages_listbox()
```

## Transition table item click handler

To handle the click event for a transition table item, the `on_transition_table_item_click()` method is called.

```python
def on_transition_table_item_click(self):
```

The first step is to identify the row under the mouse click.

```python
selected_item = self.transitions_table.identify_row(event.y)
```

If the row is already selected, it is deselected. Otherwise it is selected.

```python
if selected_item in self.transitions_table.selection():
    self.transitions_table.selection_remove(selected_item)
else:
    self.transitions_table.selection_add(selected_item)
```

With this, the transition table behaves like a normal listbox.

We can retrieve the - updated - list of selected rows by calling the `selection()` method.

```python
selected_items = self.transitions_table.selection()
```

The `selected_items` variable is a list of the indices of the selected rows. To store the actual transitions, the method iterates over the indices and retrieves the row values.

```python
row_values = [self.transitions_table.item(item, "values") for item in selected_items]
```

This list contains the values of the selected rows. The values are a tuple of the source state, target state, interface and message. This must be used to determine whether all the messages of a specific transition are selected.

To retrieve all the transitions that are associated with the selected rows, a set is created of the unique source and target state pairs.

```python
unique_source_target_pairs = set((row[0], row[1]) for row in row_values)
```

The method then iterates over the `unique_source_target_pairs` set and retrieves the transitions from the `PlantUMLManager` object.

```python
transitions = [self.plantuml_manager.get_transition(source_state, target_state) for source_state, target_state in unique_source_target_pairs]
```

First we deselect all the transitions in the `PlantUMLManager` object.

```python
self.plantuml_manager.deselect_elements(transitions, ElementType.TRANSITION)
```

We now are going to select those transitions for which all messages are selected and store it in the `selected_transitions` list, which is first initialized as an empty list.

```python
selected_transitions = []
```

For each element in the `transitions` list, the method checks whether all the messages are selected. This is done by iterating over the `transitions` list.

```python
for transition in transitions:
```

For each transition, the method retrieves the `source_state` and `target_state` and then retrieves all row values that belong to the same source and target state pair.

```python
    source_state = transition.source_state
    target_state = transition.target_state
    row_values = [self.transitions_table.item(item, "values") for item in selected_items if self.transitions_table.item(item, "values")[0] == source_state and self.transitions_table.item(item, "values")[1] == target_state]
```

Then the method checks whether all the messages are selected, which can simply be done by checking whether the number of row values is equal to the number of messages in the transition. If this is the case, the transition is added to the `selected_transitions` list.

```python
    if len(row_values) == len(transition.messages):
        selected_transitions.append(transition)
```

Finally, the method selects the transitions in the `PlantUMLManager` object.

```python
self.plantuml_manager.select_elements(selected_transitions, ElementType.TRANSITION)
```

If there were transitions selected, the `PlantUMLManager` object is notified that the selection has changed because the transition must be indicated in the diagram.

```python
if len(selected_transitions) > 0:
    self.plantuml_manager.notify_selection_change()
```

## Diagram canvas click handler

To handle the click event for the diagram canvas, the `on_diagram_canvas_click()` method is called.

```python
def on_diagram_canvas_click(self):
```

The method performs the following steps:

1. Retrieve the coordinates of the mouse click.
2. Retrieve the element at the coordinates.
3. If no element is found, deselect all elements and return.
4. If an element is found, its selection is toggled.

These steps are implemented as described below.

The first step is to retrieve the coordinates of the mouse click.

```python
x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
```

This is then used to retrieve the element at the coordinates.

```python
element = self.plantuml_manager.get_element_at_coordinates(x, y)
```

If no element is found, deselect all elements and return.

```python
if element is None:
    self.deselect_all_elements()
    return
```

If an element is found, the method toggles the selection of the element by calling the [`toggle_element_selection()`](#toggle-element-selection) method.

```python
self.toggle_element_selection(element)
```

## Toggle element selection

To toggle the selection of an element, the `toggle_element_selection()` method is called.

```python
def toggle_element_selection(self, element: Element):
```

The `element` parameter is the element to toggle the selection of.

The method must perform the following steps:

1. Toggle the selection of the element in the `PlantUMLManager` object.
2. Notify the `PlantUMLManager` object that the selection has changed.
3. Update the diagram canvas to indicate the selected elements.
4. Update the listbox - or transition table - to indicate the selected elements.

These steps are implemented as described below.

The first step is to toggle the selection of the element in the `PlantUMLManager` object.

```python
self.plantuml_manager.toggle_element_selection(element)
```

The second step is to notify the `PlantUMLManager` object that the selection has changed.

```python
self.plantuml_manager.notify_selection_change()
```

The third step is to update the diagram canvas to indicate the selected elements.

```python
self.show_diagram()
```

The fourth step is to update the listboxes - or transition table - to indicate the selected elements.

```python
self.update_listboxes()
```

Then, depending on the type of the element, the method 































































## Choice points listbox click handler


## Interfaces listbox click handler


## Messages listbox click handler






























The method handles the click event for the listbox items.

```python
if listbox == self.states_listbox:
    self.on_states_listbox_item_click(item)
elif listbox == self.choice_points_listbox:
    self.on_choice_points_listbox_item_click(item)
elif listbox == self.interfaces_listbox:
    self.on_interfaces_listbox_item_click(item)
elif listbox == self.messages_listbox:
    self.on_messages_listbox_item_click(item)
```















## Menu item click handler

The `on_menu_item_click()` method is called when a menu item is clicked.

```python
def on_menu_item_click(self, item: str):
```

The method handles the click event for the menu items.

```python
if item == "New":
    self.create_new_diagram()
elif item == "Save":
    self.save_diagram()
elif item == "Save As":
    self.save_diagram_as()
elif item == "Open":
    self.open_diagram()
elif item == "Exit":
    self.exit_application()
elif item == "Change name":
    self.change_diagram_name()
elif item == "Change transition font size":
    self.change_transition_font_size()
elif item == "Change state font size":
    self.change_state_font_size()
elif item == "About":
    self.show_about_dialog()
```










## Show diagram

To show a diagram in the diagram canvas, the `show_diagram()` method is called.

```python
def show_diagram(self):
```

Because the image to show is always the one showing the elements that are selected, the method retrieves the diagram image from the `selected_indication_diagram` from the `PlantUMLManager` object.

```python
image = self.plantuml_manager.selected_indication_diagram.rendered_image
```

The method then converts the image to a format `ImageTk.PhotoImage` can use. This is necessary because the `canvas.create_image()` method requires an `ImageTk.PhotoImage` object. The image is stored in the `diagram_canvas_image` attribute to prevent it from being garbage collected.

```python
self.diagram_canvas_image = ImageTk.PhotoImage(image)
```

Finally, the method places the image in the diagram canvas.

```python
self.canvas.create_image(0, 0, anchor=tk.NW, image=self.diagram_canvas_image)
```

## Add element

To add an element to the diagram, the `add_element()` method is called.

```python
def add_element(self, new_element: Element):
```

The first step is to get a reference to the elements mapping and the listbox.

```python
elements = self.elements[new_element.element_type]
elements_listbox = self.element_listbox[element.element_type]
```

The method adds the element to the `PlantUMLManager` object and updates the diagram canvas and the appropriate listbox.

```python
self.plantuml_manager.add_element(element)
```

The first step is to retrieve the string representation of the element (e.g. the question of a choice point).

```python
string_representation = element.get_string_representation()
```

Next, the string must be used to determine the index of the element in the appropriate `elements` list. This can be done using the fact that the `elements` list is ordered alphabetically. To do this, the method iterates over the list and compares the string representation to the elements in the list and returns the index of the element.

```python
index = 0
for i, element in enumerate(elements):
    if element[0].get_string_representation() > string_representation:
        index = i
        break
else:
    index = len(elements)
```

Now that the index is known, the element can be added to the `elements` list.

```python
elements.insert(index, new_element)
```

At the same index, the string can be added to the appropriate listbox.

```python
elements_listbox.insert(index, string_representation)
```

## Add state

To add a state to the diagram, the `add_state()` method is called.

```python
def add_state(self, new_state: State):
```

The method can call the generic [`add_element()`](#add-element) method.

```python
self.add_element(new_state)
```

Because the state is a visual element, the method must also update the diagram canvas and the states listbox.

```python
self.show_diagram()
```

## Add choice point

To add a choice point to the diagram, the `add_choice_point()` method is called.

```python
def add_choice_point(self, new_choice_point: ChoicePoint):
```

The method can call the generic [`add_element()`](#add-element) method.

```python
self.add_element(new_choice_point)
```

Because the choice point is a visual element, the method must also update the diagram canvas and the choice points listbox.

```python
self.show_diagram()
```

## Add interface

To add an interface to the diagram, the `add_interface()` method is called.

```python
def add_interface(self, new_interface: Interface):
```

The method can call the generic [`add_element()`](#add-element) method.

```python
self.add_element(new_interface)
``` 

Because the interface is not a visual element, the method does not need to update the diagram canvas.

## Add message

To add a message to the diagram, the `add_message()` method is called.

```python
def add_message(self, new_message: Message):
```

The method can call the generic [`add_element()`](#add-element) method.

```python
self.add_element(new_message)
```

Note that this is possible because a message can only be added when the interface is selected.

Since the message is not a visual element, the method does not need to update the diagram canvas.

## Add transition

To add a transition to the diagram, the `add_transition()` method is called.

```python
def add_transition(self, new_transition: Transition):
```

The first step is to get a reference to the list of transitions.

```python
transitions = self.elements[ElementType.TRANSITION]
```

The method then adds the transition to the `PlantUMLManager` object.

```python
self.plantuml_manager.add_element(new_transition)
```

Next, the index of the transition must be determined in the `transitions` list. To do this, the method iterates over the list and compares the transition to the elements in the list and returns the index of the new transition.

```python
index = 0
for i, transition in enumerate(transitions):
    if (
        transition.source_state,
        transition.target_state,
        transition.interface,
        transition.message
    ) > (
        new_transition.source_state,
        new_transition.target_state,
        new_transition.interface,
        new_transition.message
    ):
        index = i
        break
else:
    index = len(transitions)
```

With the index known, the transition can be added to the `transitions` list.

```python
transitions.insert(index, new_transition)
```

At the same index, the transition can be added to the table.

```python
self.transitions_table.insert("", tk.END, values=(new_transition.source_state, new_transition.target_state, new_transition.interface, new_transition.message))
```

The method also updates the diagram canvas because the transition is a visual element.

```python
self.show_diagram()
```

## Delete element

To delete an element, the `delete_element()` method is called.

```python
def delete_element(self, element: Element):
```

The method first removes the element from the `PlantUMLManager` object.

```python
self.plantuml_manager.delete_element(element)
```

In order to be able to delete the element from the listbox, the method must first get the index of the element in the list.

```python
index = self.elements[element.element_type].index(element)
```

With the index known, the element can be deleted from the listbox or the table.

```python
if element.element_type in [ElementType.STATE, ElementType.CHOICE_POINT]:
    self.elements_listbox[element.element_type].delete(index)
else:
    self.transitions_table.delete(index)
```

The element can also be deleted from the elements list.

```python
self.elements[element.element_type].remove(element)
```

If the element is a visual element, i.e. a state or a choice point, the method must also update the diagram canvas.

```python
if element.element_type in [ElementType.STATE, ElementType.CHOICE_POINT]:
    self.show_diagram()
```

## Appendix - `create_image()`

The `canvas.create_image()` method is part of the `tkinter` module in Python, which is used to create graphical user interfaces (GUIs). This method allows you to display images on a `Canvas` widget.

### Syntax

```python
canvas.create_image(x, y, **options)
```

- **`x`**, **`y`**: Coordinates on the canvas where the image will be placed. The position is determined based on the `anchor` option.
- **`options`**: Additional configuration options for the image.

### Key Options

1. **`image`**: The `PhotoImage` or `BitmapImage` object to display.
2. **`anchor`**: Defines how the image is positioned relative to the `(x, y)` coordinates. Default is `center`. Other values include `nw`, `n`, `ne`, `w`, `e`, `sw`, `s`, and `se`.

### Example Code

```python
import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Canvas Image Example")

# Create a canvas widget
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Load an image
image = tk.PhotoImage(file="example.png")

# Add the image to the canvas
canvas.create_image(200, 200, image=image, anchor="center")

# Run the application
root.mainloop()
```

### Notes

1. The `PhotoImage` class supports `.png`, `.gif`, and `.ppm/.pgm` formats.
2. You must keep a reference to the `PhotoImage` object (e.g., by assigning it to a variable). If it is garbage-collected, the image will not display.
3. For image formats not supported by `PhotoImage`, you can use the `Pillow` library to load images and convert them to a `PhotoImage` object.

### Example with `Pillow`

```python
from tkinter import Tk, Canvas
from PIL import Image, ImageTk

# Create the main window
root = Tk()

# Create a canvas widget
canvas = Canvas(root, width=400, height=400)
canvas.pack()

# Load an image using Pillow
image = Image.open("example.jpg")
photo = ImageTk.PhotoImage(image)

# Add the image to the canvas
canvas.create_image(200, 200, image=photo, anchor="center")

# Keep a reference to the image to prevent garbage collection
canvas.image = photo

# Run the application
root.mainloop()
```

This method is useful for creating GUIs where you want to display images as part of a graphical layout.









