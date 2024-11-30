# PlantUMLManager

_The `PlantUMLManager` class is responsible for loading and saving the PlantUML code, creating the selection mask and updating the diagram canvas with the new selection mask._

## Attributes

The class has the following attributes:

- **Diagrams**:
  - `state_diagram`: a `Diagram` object containing the PlantUML code and rendered image of the state diagram.
  - `selection_mask_diagram`: a `Diagram` object containing the PlantUML code and rendered image of the selection mask.
  - `selection_indication_diagram`: a `Diagram` object containing the PlantUML code and rendered image of the selection indication.

- **Elements**:
  - `interfaces`: a list of `Interface` objects.
  - `messages`: a list of `Message` objects.
  - `states`: a list of `State` objects.
  - `choice_points`: a list of `ChoicePoint` objects.
  - `transitions`: a list of `Transition` objects.

- **Administration**:
  - `elements`: the list of all elements.
  - `selected_element_identifiers`: a list of the identifiers of the selected elements.

- **History**:
  - `history`: a list of PlantUML code strings representing the history.
  - `current_index`: an integer representing the current index in the history.

The class has the following method to load a diagram:

- `load_diagram(plantuml_code: str) -> bool`: loads the PlantUML code and updates all the diagrams. It returns `True` if successful and `False` otherwise, e.g. when the PlantUML code is invalid.

The following method is used to get the element at the given coordinates:

- `get_element_at(x: int, y: int) -> Element | None`: returns the element at the given coordinates or `None` if no element is at the given coordinates.

The following methods are used to add new elements to the diagram. They return the element if successful and `None` otherwise (e.g. the element already exists):

- `add_interface(interface_name: str) -> Interface | None`: adds a new interface to the diagram.
- `add_message(interface_name: str, message_name: str) -> Message | None`: adds a new message to the diagram.
- `add_state(state_name: str, display_name: str = "") -> State | None`: adds a new state to the diagram.
- `add_choice_point(choice_point_name: str, question: str = "") -> ChoicePoint | None`: adds a new choice-point to the diagram.
- `add_transition(source_name: str, target_name: str, connector_type: str, connector_length: int, messages: List[str]) -> Transition | None`: adds a new transition to the diagram.

The following methods are used to update elements, and return `True` if successful and `False` otherwise (e.g. the element does not exist):

- `update_state(state: State, new_name: str | None = None, new_display_name: str | None = None) -> bool`: updates the name and/or display name of a state. When the name is updated, it also updates the name of the source and target states of all transitions that have the state as source or target.
- `update_choice_point(choice_point: ChoicePoint, new_name: str | None = None, new_question: str | None = None) -> bool`: updates the name and/or question of a choice-point if provided. When the name is updated, it also updates the name of the source state of all transitions that have the choice-point as source.
- `update_transition(transition: Transition, new_connector_type: str | None = None, new_connector_length: int | None = None, new_messages: List[Message] | None = None) -> bool`: updates the connector type, length or messages of a transition when provided.

All these methods will result in the PlantUML code of the `state_diagram` being updated, which in turn updates the rendered image and the selection mask and the selection indication diagram.

For handling selection of diagram elements (states, choice-points, transitions), the following methods are used:

- `select_element(element: Element)`: selects the given element. This will update the `selected_element_identifiers` list and the `selection_indication_diagram`.
- `deselect_element(element: Element)`: deselects the given element. This will remove the element from the `selected_element_identifiers` list and update the `selection_indication_diagram`.
- `get_selected_elements() -> List[Element]`: returns the list of selected elements.
- `deselect_all_elements()`: deselects all elements. This will clear the `selected_element_identifiers` list and update the `selection_indication_diagram`.

Note that the selection of protocol elements (interfaces and messages) is handled outside the `PlantUMLManager` class as it does not change the rendered image of the diagram.

The following method is used to delete elements from the diagram:

- `delete_elements(elements: List[Element])`: deletes the given elements from the diagram. This will update the PlantUML code of the `state_diagram`, which in turn updates the rendered image, the selection mask and the selection indication diagram.

The following methods are used to manage the history:

- `add_history(plantuml_code: str)`: adds a new entry to the history. It will also increment the `current_index` and remove any future entries in the history, i.e. the history will only contain the current entry and all previous entries.
- `undo() -> str | None`: undoes the last action, by decrementing the `current_index` and returning the string at the new `current_index` or `None` if the `current_index` is 0 (the first action in the history).
- `redo() -> str | None`: redoes the last action, by incrementing the `current_index` and returning the string at the new `current_index` or `None` if the `current_index` is equal to the length of the history (the last action in the history).