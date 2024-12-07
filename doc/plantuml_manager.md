# PlantUMLManager

_The `PlantUMLManager` class is responsible for starting the local PlantUML server, loading and saving the PlantUML code, creating the selection mask and updating the diagram canvas with the new selection indication._

## Dependencies

Running the PlantUML server locally is done by executing a Java command. To be able to execute this command but also properly halt the process, the following dependencies are required:

- `atexit` : for registering a cleanup function that will be called when the program exits.
- `subprocess` : for executing the Java command in the background.

```python
import atexit
import subprocess
```

## Proprietary dependencies

The `PlantUMLManager` class depends on the `Diagram` class and the `Element` classes.

```python
from diagram import Diagram
from elements import Interface, Message, State, ChoicePoint, Transition, CodeType
```

## Constants

The `PlantUMLManager` class has the following constants:

- `PLANTUML_PORT`: an integer representing the port number on which the local PlantUML server listens.

```python
PLANTUML_PORT = 9000
```

For checking and parsing the PlantUML code, the `PlantUMLManager` class has the following constants:

- `SECTION_START_INDICATOR`: a string containing the indicator for the start of a new section.

```python
SECTION_START_INDICATOR = "'== "
```

- `SECTION_END_INDICATOR`: a string containing the indicator for the end of a section.

```python
SECTION_END_INDICATOR = " =="
```

- `HEADER_PLANTUML_CODE`: a string containing the PlantUML code for the header.

```python
HEADER_PLANTUML_CODE = """@startuml
'== Formatting ==
hide empty description
skinparam Arrow {
  FontSize 9
}
skinparam State {
  FontSize 12
}
"""
```

- `HEADER_MASKED_PLANTUML_CODE`: a string containing the PlantUML code for the header with masked font colors.

```python
HEADER_MASKED_PLANTUML_CODE = """@startuml
'== Formatting ==
hide empty description
skinparam Arrow {
  FontSize 9
  FontColor #00000000
}
skinparam State {
  FontSize 12
  FontColor #00000000
}
"""
```

- `DEFAULT_MESSAGES_PLANTUML_CODE`: a string containing the PlantUML code for the default messages.

```python
DEFAULT_MESSAGES_PLANTUML_CODE = """
'== Default messages ==
!$Timeout = Timeout
!$No = No
!$Yes = Yes
"""
```

- `INTERFACES_PLANTUML_CODE`: a string containing the PlantUML code for the interfaces.

```python
INTERFACES_PLANTUML_CODE = """'== Interfaces ==
"""
```

- `MESSAGES_PLANTUML_CODE`: a string containing the PlantUML code for the messages.

```python
MESSAGES_PLANTUML_CODE = """'== Messages ==
"""
```

- `COMPONENT_PLANTUML_CODE`: a string containing the PlantUML code for the component.

```python
COMPONENT_PLANTUML_CODE = """'== Component ==
"""
```

- `STATES_PLANTUML_CODE`: a string containing the PlantUML code for the states.

```python
STATES_PLANTUML_CODE = """'== States ==
"""
```

- `CHOICE_POINTS_PLANTUML_CODE`: a string containing the PlantUML code for the choice-points.

```python
CHOICE_POINTS_PLANTUML_CODE = """'== Choice-points ==
"""
```

- `TRANSITIONS_PLANTUML_CODE`: a string containing the PlantUML code for the transitions.

```python
TRANSITIONS_PLANTUML_CODE = """'== Transitions ==
"""
```

- `FOOTER_PLANTUML_CODE`: a string containing the PlantUML code for the footer.

```python
FOOTER_PLANTUML_CODE = """'== Footer ==
@enduml"""
```

- `SECTIONS`: a list of the section indicators.

```python
SECTIONS = [HEADER_PLANTUML_CODE, DEFAULT_MESSAGES_PLANTUML_CODE, INTERFACES_PLANTUML_CODE, MESSAGES_PLANTUML_CODE, COMPONENT_PLANTUML_CODE, STATES_PLANTUML_CODE, CHOICE_POINTS_PLANTUML_CODE, TRANSITIONS_PLANTUML_CODE, FOOTER_PLANTUML_CODE]
```

## Attributes

The class has the following attributes:

- `process`: a `subprocess.Popen` object representing the local PlantUML server.
- `plantuml_endpoint`: a string representing the endpoint of the local PlantUML server.
- `component_name`: a string representing the name of the component.
- `state_diagram`: a `Diagram` object containing the PlantUML code and rendered image of the state diagram.
- `selection_mask_diagram`: a `Diagram` object containing the PlantUML code and rendered image of the selection mask.
- `selection_indication_diagram`: a `Diagram` object containing the PlantUML code and rendered image of the selection indication.
- `interfaces`: a list of `Interface` objects.
- `messages`: a list of `Message` objects.
- `states`: a list of `State` objects.
- `choice_points`: a list of `ChoicePoint` objects.
- `transitions`: a list of `Transition` objects.
- `elements`: the list of all elements.
- `selected_element_identifiers`: a list of the identifiers of the selected elements.
- `history`: a list of PlantUML code strings representing the history.
- `current_history_index`: an integer representing the current index in the history.

## Constructor

The constructor of the class takes no arguments.

```python
def __init__(self):
```

The first step is to start the local PlantUML server by executing the Java command in the background. This is done in the [`start_plantuml_server()`](#start-the-local-plantuml-server) method which returns the `subprocess.Popen` object representing the local PlantUML server.

```python
self.process = self.start_plantuml_server(PLANTUML_PORT)
```

Then the PlantUML endpoint is set, which will be used by the `Diagram` objects to generate the PlantUML code and rendered images.

```python
self.plantuml_endpoint = f"http://localhost:{PLANTUML_PORT}/png/"
```

Next the attributes are initialized with the default values, starting with the component name which is given the value "Component Name".

```python
self.component_name = "Component Name"
```

Next the `Diagram` objects are initialized with the PlantUML endpoint.

```python
self.state_diagram = Diagram(self.plantuml_endpoint)
self.selection_mask_diagram = Diagram(self.plantuml_endpoint)
self.selection_indication_diagram = Diagram(self.plantuml_endpoint)
```

Next the lists of elements are initialized that are all still empty:

```python 
self.interfaces = []
self.messages = []
self.states = []
self.choice_points = []
self.transitions = []
self.elements = []
```

To keep track of the selected elements, the `selected_element_identifiers` list is initialized as empty:

```python
self.selected_element_identifiers = []
```

Finally, to keep track of the history, the `history` list is initialized as empty and the `current_history_index` is set to 0:

```python
self.history = []
self.current_history_index = 0
```

## Methods

To start the local PlantUML server, the following methods are used:

- [`start_plantuml_server()`](#start-the-local-plantuml-server): starts the local PlantUML server.
- [`cleanup()`](#cleanup-function): terminates the local PlantUML server when the program exits.
When the PlantUML code is loaded, the following methods can be used:

- [`set_elements()`](#set-elements): sets the all the list.

To retrieve the specific elements from the PlantUML code, the following method is used:

- [`get_interfaces_from_plantuml_code(plantuml_code: str) -> List[Interface]`](#get-interfaces-from-plantuml-code): returns the interfaces from the PlantUML code.
- [`get_messages_from_plantuml_code(plantuml_code: str) -> List[Message]`](#get-messages-from-plantuml-code): returns the messages from the PlantUML code.
- [`get_component_from_plantuml_code(plantuml_code: str) -> str`](#get-component-from-plantuml-code): returns the component name from the PlantUML code.
- [`get_states_from_plantuml_code(plantuml_code: str) -> List[State]`](#get-states-from-plantuml-code): returns the states from the PlantUML code.
- [`get_choice_points_from_plantuml_code(plantuml_code: str) -> List[ChoicePoint]`](#get-choice-points-from-plantuml-code): returns the choice-points from the PlantUML code.
- [`get_transitions_from_plantuml_code(plantuml_code: str) -> List[Transition]`](#get-transitions-from-plantuml-code): returns the transitions from the PlantUML code.

The following method is used to load the PlantUML code and update all the diagrams:

- [`load_diagram(plantuml_code: str) -> bool`](#load-diagram): loads the PlantUML code and updates all the diagrams. It returns `True` if successful and `False` otherwise, e.g. when the PlantUML code is invalid.
- [`validate_plantuml_code(plantuml_code: str) -> bool`](#validate-plantuml-code): validates the PlantUML code. It returns `True` if the PlantUML code is valid and `False` otherwise.

The following method is used to get the element at the given coordinates:

- [`get_element_at(x: int, y: int) -> Element | None`](#get-an-element-at-given-coordinates): returns the element at the given coordinates or `None` if no element is at the given coordinates.

The following methods are used to add new elements to the diagram. They return the element if successful and `None` otherwise (e.g. the element already exists):

- [`add_interface(interface_name: str) -> Interface | None`](#add-a-new-interface): adds a new interface to the diagram.
- [`add_message(interface_name: str, message_name: str) -> Message | None`](#add-a-new-message): adds a new message to the diagram.
- [`add_state(state_name: str, display_name: str = "") -> State | None`](#add-a-new-state): adds a new state to the diagram.
- [`add_choice_point(choice_point_name: str, question: str = "") -> ChoicePoint | None`](#add-a-new-choice-point): adds a new choice-point to the diagram.
- [`add_transition(source_name: str, target_name: str, connector_type: str, connector_length: int) -> Transition | None`](#add-a-new-transition): adds a new - empty - transition to the diagram.

The following methods are used to update elements, and return `True` if successful and `False` otherwise (e.g. the element does not exist or the new name is already used by another element):

- [`update_state(state: State, new_name: str | None = None, new_display_name: str | None = None) -> bool`](#update-a-state): updates the name and/or display name of a state. When the name is updated, it also updates the name of the source and target states of all transitions that have the state as source or target.
- [`update_choice_point(choice_point: ChoicePoint, new_name: str | None = None, new_question: str | None = None) -> bool`](#update-a-choice-point): updates the name and/or question of a choice-point if provided. When the name is updated, it also updates the name of the source state of all transitions that have the choice-point as source.
- [`update_transition(transition: Transition, new_connector_type: str | None = None, new_connector_length: int | None = None, new_messages: List[Message] | None = None) -> bool`](#update-a-transition): updates the connector type, length or messages of a transition when provided.

All these methods will result in the PlantUML code of the `state_diagram` being updated, which in turn updates the rendered image and the selection mask and the selection indication diagram.

For handling selection of diagram elements (states, choice-points, transitions), the following methods are used:

- [`select_element(element: Element)`](#select-an-element): selects the given element. This will update the `selected_element_identifiers` list and the `selection_indication_diagram`.
- [`deselect_element(element: Element)`](#deselect-an-element): deselects the given element. This will remove the element from the `selected_element_identifiers` list and update the `selection_indication_diagram`.
- [`get_selected_elements() -> List[Element]`](#get-the-selected-elements): returns the list of selected elements.
- [`deselect_all_elements()`](#deselect-all-elements): deselects all elements. This will clear the `selected_element_identifiers` list and update the `selection_indication_diagram`.

Note that the selection of protocol elements (interfaces and messages) is handled outside the `PlantUMLManager` class as it does not change the rendered image of the diagram.

The following method is used to delete elements from the diagram:

- [`delete_elements(elements: List[Element])`](#delete-elements): deletes the given elements from the diagram. This will update the PlantUML code of the `state_diagram`, which in turn updates the rendered image, the selection mask and the selection indication diagram.
- [`delete_interface(interface: Interface)`](#delete-an-interface): deletes the given interface from the diagram. This will update the PlantUML code of the `state_diagram`, which in turn updates the rendered image, the selection mask and the selection indication diagram.
- [`delete_message(message: Message)`](#delete-a-message): deletes the given message from the diagram. This will update the PlantUML code of the `state_diagram`, which in turn updates the rendered image, the selection mask and the selection indication diagram.
- [`delete_state(state: State)`](#delete-a-state): deletes the given state from the diagram. This will update the PlantUML code of the `state_diagram`, which in turn updates the rendered image, the selection mask and the selection indication diagram.
- [`delete_choice_point(choice_point: ChoicePoint)`](#delete-a-choice-point): deletes the given choice-point from the diagram. This will update the PlantUML code of the `state_diagram`, which in turn updates the rendered image, the selection mask and the selection indication diagram.
- [`delete_transition(transition: Transition)`](#delete-a-transition): deletes the given transition from the diagram. This will update the PlantUML code of the `state_diagram`, which in turn updates the rendered image, the selection mask and the selection indication diagram.

The following methods are used to manage the history:

- [`add_history(plantuml_code: str)`](#add-a-new-entry-to-the-history): adds a new entry to the history. It will also increment the `current_index` and remove any future entries in the history, i.e. the history will only contain the current entry and all previous entries.
- [`undo() -> str | None`](#undo-the-last-action): undoes the last action, by decrementing the `current_index` and returning the string at the new `current_index` or `None` if the `current_index` is 0 (the first action in the history).
- [`redo() -> str | None`](#redo-the-last-action): redoes the last action, by incrementing the `current_index` and returning the string at the new `current_index` or `None` if the `current_index` is equal to the length of the history (the last action in the history).

To generate a complete PlantUML code, the following methods are used:

- [`get_plantuml_code(code_type: CodeType)`](#get-plantuml-code): returns the PlantUML code of the diagram, depending on the type of the code.

To support the PlantUML generation, the following methods are used:

- [`get_interfaces_plantuml_code(code_type: CodeType)`](#get-interfaces-plantuml-code): returns the PlantUML code for the interfaces.
- [`get_messages_plantuml_code(code_type: CodeType)`](#get-messages-plantuml-code): returns the PlantUML code for the messages.
- [`get_component_plantuml_code(code_type: CodeType)`](#get-component-plantuml-code): returns the PlantUML code for the component.
- [`get_states_plantuml_code(code_type: CodeType)`](#get-states-plantuml-code): returns the PlantUML code for the states.
- [`get_choice_points_plantuml_code(code_type: CodeType)`](#get-choice-points-plantuml-code): returns the PlantUML code for the choice-points.
- [`get_transitions_plantuml_code(code_type: CodeType)`](#get-transitions-plantuml-code): returns the PlantUML code for the transitions.

In the following sections, the methods are described in more detail.

## Start the local PlantUML server

To start the local PlantUML server, the following method is used:

```python
def start_plantuml_server(self, port: int) -> subprocess.Popen:
```

The first step is to define the command to run:

```python
command = ["java", "-jar", "plantuml.jar", f"-picoweb:{port}"]
```

Next the command is executed in the background and the process is stored in the `process` attribute to be able to terminate it when the program exits:

```python
process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
```

When the program exits, the `atexit.register()` function is used to register the [`cleanup()`](#cleanup-function) method to be called when the program exits:

```python
atexit.register(self.cleanup)
```

To allow the process to start, the program waits for 1 second:

```python
time.sleep(1)
```

Finally, the process is returned.

```python
return process
```

## Cleanup function

When the program exits, the following cleanup method is called to terminate the process:

```python
def cleanup():
```

This method first checks if the process is still running. This can be done by calling the `poll()` method of the process, which returns `None` for a running process.

```python
if not self.process.poll() is None:
    return
```

If the process is still running, it terminates the process gracefully by calling the `terminate()` method of the process:

```python
self.process.terminate()
``` 

This is a non-blocking call, so the program continues immediately. The process is then waited for to exit within a timeout period using the `wait()` method of the process. If the process does not exit within the timeout period, it forcefully kills the process by calling the `kill()` method of the process.

```python
try:
    self.process.wait(timeout=5)
except subprocess.TimeoutExpired:
    print("Forcing process kill...")
self.process.kill()
```

## Set elements

When the `state_diagram` is loaded, the `set_elements()` method is called which sets the all the lists of elements.

```python
def set_elements(self):
```

This method first clears all the lists of elements:

```python
self.interfaces.clear()
self.messages.clear()
self.states.clear()
self.choice_points.clear()
self.transitions.clear()
self.elements.clear()
self.selected_element_identifiers.clear()
```

First all the default messages are added to the `messages` list:

```python
self.messages.append(Message("Timeout"))
self.messages.append(Message("No"))
self.messages.append(Message("Yes"))
```

Next the `START` state is added to the `states` list:

```python
self.states.append(State("START"))
```

With this set, all the lists are populated with the elements from the PlantUML code, where the `+=` operator is used to add the new elements to the lists in order to keep the existing elements (if any):

```python
self.interfaces += get_interfaces_from_plantuml_code(self.state_diagram.plantuml_code)
self.messages += get_messages_from_plantuml_code(self.state_diagram.plantuml_code)
self.component_name = get_component_from_plantuml_code(self.state_diagram.plantuml_code)
self.states += get_states_from_plantuml_code(self.state_diagram.plantuml_code)
self.choice_points += get_choice_points_from_plantuml_code(self.state_diagram.plantuml_code)
self.transitions += get_transitions_from_plantuml_code(self.state_diagram.plantuml_code)
```

Now that all the lists are set, the list of elements is populated with all the elements:

```python
self.elements = self.states + self.choice_points + self.transitions + self.interfaces + self.messages
```

Note that the states are added first as the `START` state must have an identifier of 0. This now makes it possible to set the `identifiers` of the elements:

```python
for i, element in enumerate(self.elements):
    element.identifier = i
```

## Get interfaces from PlantUML code

To retrieve the interfaces from the PlantUML code, the following method is used:

```python
def get_interfaces_from_plantuml_code(plantuml_code: str) -> List[Interface]:
```

The first step is to find the location of the "Interfaces" section in the PlantUML code. This is done by finding the index of the line containing `INTERFACES_PLANTUML_CODE`:

```python
interfaces_index = self.state_diagram.plantuml_code.find(INTERFACES_PLANTUML_CODE)
```

After this line, interfaces could be specified - it could also be empty. The following code is used to extract the interfaces until an empty line is encountered or the line contains a `SECTION_START_INDICATOR`, which indicates a new section:

```python
lines = []
for line in self.state_diagram.plantuml_code[interfaces_index:].split("\n"):
    if line == "" or line.startswith(SECTION_START_INDICATOR):
        break
    lines.append(line)
```

The `lines` list now contains all the lines of the interfaces section, which are lines like the following for example:

```
!$RTx = RTx
```

The following code is used to extract the interface names from the lines after which the created list of `Interface` objects is returned:

```python
interfaces = []
for line in lines:
    interface = Interface.from_plantuml_code(line)
    interfaces.append(interface)
return interfaces
```

## Get messages from PlantUML code

To retrieve the messages from the PlantUML code, the following method is used:

```python
def get_messages_from_plantuml_code(plantuml_code: str) -> List[Message]:
```

The first step is to find the location of the "Messages" section in the PlantUML code. This is done by finding the index of the line containing `MESSAGES_PLANTUML_CODE`:

```python
messages_index = self.state_diagram.plantuml_code.find(MESSAGES_PLANTUML_CODE)
```

After this line, messages could be specified - it could also be empty. The following code is used to extract the messages until an empty line is encountered or the line contains a `SECTION_START_INDICATOR`, which indicates a new section:

```python
lines = []
for line in self.state_diagram.plantuml_code[messages_index:].split("\n"):
    if line == "" or line.startswith(SECTION_START_INDICATOR):
        break
    lines.append(line)
```

The `lines` list now contains all the lines of the messages section, which are lines like the following for example:

```
$RTx_ConnectReq = $RTx + ":" + ConnectReq
$RTx_ConnectedInd = $RTx + ":" + ConnectedInd
```

The following code is used to extract the messages from the lines after which the created list of `Message` objects is returned:

```python
messages = []
for line in lines:
    message = Message.from_plantuml_code(line)
    messages.append(message)
return messages
```

## Get component from PlantUML code

To retrieve the component name from the PlantUML code, the following method is used:

```python
def get_component_from_plantuml_code(plantuml_code: str) -> str:
```

The first step is to find the location of the "Component" section in the PlantUML code. This is done by finding the index of the line containing `COMPONENT_PLANTUML_CODE`:

```python
component_index = plantuml_code.find(COMPONENT_PLANTUML_CODE)
```

The component name is part of the line after the "Component" section. The following code is used to extract the next line after the "Component" section:

```python
component_name_line = plantuml_code[component_index+len(COMPONENT_PLANTUML_CODE):].split("\n")[0]
```

The component name can contain spaces, so multiple words, so it is retrieved between the first and second quote:

```python
component_name = component_name_line.split('"')[1]
```

Finally, the component name is returned.

```python
return component_name
```


## Get states from PlantUML code

To retrieve the states from the PlantUML code, the following method is used:

```python
def get_states_from_plantuml_code(plantuml_code: str) -> List[State]:
```

The first step is to find the location of the "States" section in the PlantUML code. This is done by finding the index of the line containing `STATES_PLANTUML_CODE`:

```python
states_index = self.state_diagram.plantuml_code.find(STATES_PLANTUML_CODE)
```

After this line, states could be specified - it could also be empty. The following code is used to extract the states until an empty line is encountered or the line contains a `SECTION_START_INDICATOR`, which indicates a new section:

```python
lines = []
for line in self.state_diagram.plantuml_code[states_index:].split("\n"):
    if line == "" or line.startswith(SECTION_START_INDICATOR):
        break
    lines.append(line)
```

The `lines` list now contains all the lines of the states section, which are lines like the following for example:

```
state Connecting
state Advertising
state StoppedProcessing as "Stopped\nProcessing"
```

The following code is used to extract the states from the lines after which the created list of `State` objects is returned:

```python
states = []
for line in lines:
    state = State.from_plantuml_code(line)
    states.append(state)
return states
```

## Get choice-points from PlantUML code

To retrieve the choice-points from the PlantUML code, the following method is used:

```python
def get_choice_points_from_plantuml_code(plantuml_code: str) -> List[ChoicePoint]:
```

The first step is to find the location of the "Choice-points" section in the PlantUML code. This is done by finding the index of the line containing `CHOICE_POINTS_PLANTUML_CODE`:

```python
choice_points_index = self.state_diagram.plantuml_code.find(CHOICE_POINTS_PLANTUML_CODE)
```

After this line, choice-points could be specified - it could also be empty. The following code is used to extract the choice-points until an empty line is encountered or the line contains a `SECTION_START_INDICATOR`, which indicates a new section:

```python
lines = []
for line in self.state_diagram.plantuml_code[choice_points_index:].split("\n"):
    if line == "" or line.startswith(SECTION_START_INDICATOR):
        break
    lines.append(line)
```

The `lines` list now contains all the lines of the choice-points section, which are lines like the following for example:

```
state CP_Whitelisted as "Is\nWhitelisted?"
```

The following code is used to extract the choice-points from the lines after which the created list of `ChoicePoint` objects is returned:

```python
choice_points = []
for line in lines:
    choice_point = ChoicePoint.from_plantuml_code(line)
    choice_points.append(choice_point)
return choice_points
```

## Get transitions from PlantUML code

To retrieve the transitions from the PlantUML code, the following method is used:

```python
def get_transitions_from_plantuml_code(plantuml_code: str) -> List[Transition]:
```

The first step is to find the location of the "Transitions" section in the PlantUML code. This is done by finding the index of the line containing `TRANSITIONS_PLANTUML_CODE`:

```python
transitions_index = self.state_diagram.plantuml_code.find(TRANSITIONS_PLANTUML_CODE)
```

After this line, transitions could be specified - it could also be empty. The following code is used to extract the transitions until an empty line is encountered or the line contains a `SECTION_START_INDICATOR`, which indicates a new section:

```python
lines = []
for line in self.state_diagram.plantuml_code[transitions_index:].split("\n"):
    if line == "" or line.startswith(SECTION_START_INDICATOR):
        break
    lines.append(line)
```

The `lines` list now contains all the lines of the transitions section, which are lines like the following for example:

```
Connecting -> Advertising : $RTx_ConnectReq\n$RTx_ConnectInd
Advertising -> StoppedProcessing : $RTx_ConnectedInd\n$RTx_ConnectedInd
StoppedProcessing -> Advertising : $Timeout
```

The following code is used to extract the transitions from the lines after which the created list of `Transition` objects is returned:

```python
transitions = []
for line in lines:
    transition = Transition.from_plantuml_code(line)
    transitions.append(transition)
return transitions
```

## Load diagram

The following method is used to load the diagram given a PlantUML code:

```python
def load_diagram(plantuml_code: str) -> bool:
```

The method first checks if the PlantUML code is valid by calling the `validate_plantuml_code()` method. If it is not valid, `False` is returned.

```python
if not self.validate_plantuml_code(plantuml_code):
    return False
```

When the PlantUML code is valid, it can be loaded into the `state_diagram`. If this is not successful, the method will exit as well.

```python
if not self.state_diagram.set_plantuml_code(plantuml_code):
    return False
```

When the PlantUML code is loaded successfully, the `set_elements()` method is called to set the elements of the diagram.

```python
self.set_elements()
```

With the elements set, the PlantUML code can be determined for the other diagrams and set via the `load_diagram()` method which also checks if the PlantUML code is valid. If either one of the PlantUML codes is not valid, the method will exit and return `False`.

```python
if not self.selection_mask_diagram.set_plantuml_code(self.get_plantuml_code(CodeType.SELECTION_MASK)):
    return False
if not self.selection_indication_diagram.set_plantuml_code(self.get_plantuml_code(CodeType.SELECTION_INDICATION)):
    return False
```

Finally, `True` is returned to indicate that the diagram was loaded successfully.

```python
return True
```

## Validate PlantUML code

To validate the PlantUML code, the following method is used:

```python
def validate_plantuml_code(plantuml_code: str) -> bool:
```

The first step is to create a temporary diagram and load the PlantUML code into it. If this is not successful, `False` is returned.

```python
diagram = Diagram()
if not diagram.load_diagram(plantuml_code):
    return False
```

This checks that the PlantUML code contains valid PlantUML code. However, it does not check whether it contains a correctly formatted state diagram, i.e. whether it contains all the sections and whether they are in the correct order.

The following code is used to check whether the PlantUML code contains all the sections and whether they are in the correct order:

```python
previous_index = -1
for section in SECTIONS:
    index = plantuml_code.find(section)
    if index == -1 or index < previous_index:
        return False
    previous_index = index
```

Finally, `True` is returned to indicate that the PlantUML code is valid.

```python
return True
```

## Get an element at given coordinates

The following method is used to get the element at the given coordinates:

```python
def get_element_at(x: int, y: int) -> Element | None:
```

To retrieve the element at the given coordinates, the color of the pixel at the given coordinates is retrieved from the `selection_mask_diagram`.

```python
rgb_color = self.selection_mask_diagram.rendered_image.getpixel((x, y))  
```

If the image has an alpha channel (RGBA), the result will be a 4-tuple (R, G, B, A). In that case, the alpha value can be ignored:

```python
if len(rgb_color) == 4:
    rgb_color = rgb_color[:3]
```

The RGB tuple can then be converted to a value to be used as an index for the `elements` list.

```python
index = rgb_color[0] * 256 * 256 + rgb_color[1] * 256 + rgb_color[2]
```

The element at the given index is then returned only if the index is valid.

```python
return self.elements[index] if 0 <= index < len(self.elements) else None
```

## Add a new interface

The following method is used to add a new interface to the diagram: 

```python
def add_interface(interface_name: str) -> Interface | None:
```

First it is checked if the interface name already exists by checking if an interface with the given name is in the `interfaces` list:

```python
if any(interface.name == interface_name for interface in self.interfaces):
    return None
```

If the interface name does not exist, a new `Interface` object is created with the given name and added to the `interfaces` list:

```python
interface = Interface(interface_name)
self.interfaces.append(interface)
return interface
```

## Add a new message

The following method is used to add a new message to the diagram:

```python
def add_message(interface_name: str, message_name: str) -> Message | None:
```

First it is checked if the message name already exists by checking if a message with the given interface variable name and message name is in the `messages` list:

```python
if any(message.interface_name == interface_name and message.name == message_name for message in self.messages):
    return None
```

If the message name does not exist, a new `Message` object is created with the given interface variable name and message name and added to the `messages` list:

```python
message = Message(interface_name, message_name)
self.messages.append(message)
return message
```

## Add a new state

The following method is used to add a new state to the diagram:

```python
def add_state(state_name: str, display_name: str = "") -> State | None:
```

First it is checked if the state name already exists by checking if a state with the given name is in the `states` list:

```python
if any(state.name == state_name for state in self.states):
    return None
```

If the state name does not exist, a new `State` object is created with the given name and added to the `states` list:

```python
state = State(state_name, display_name)
self.states.append(state)
return state
```

## Add a new choice-point

The following method is used to add a new choice-point to the diagram:

```python
def add_choice_point(choice_point_name: str, question: str = "") -> ChoicePoint | None:
```

First it is checked if the choice-point name already exists by checking if a choice-point with the given name is in the `choice_points` list:

```python
if any(choice_point.name == choice_point_name for choice_point in self.choice_points):
    return None
```

If the choice-point name does not exist, a new `ChoicePoint` object is created with the given name and added to the `choice_points` list:

```python
choice_point = ChoicePoint(choice_point_name, question)
self.choice_points.append(choice_point)
return choice_point
```

## Add a new transition

The following method is used to add a new - empty - transition to the diagram:

```python
def add_transition(source_name: str, target_name: str, connector_type: str, connector_length: int) -> Transition | None:
```

A transition can always be added because it is possible to add messages later and it is allowed to have multiple transitions between the same source and target. This is because the developer could decide this when editing the diagram for clarity reasons.

A new `Transition` object is created with the given source, target, connector type, connector length and an empty list of messages and added to the `transitions` list:

```python
transition = Transition(source_name, target_name, connector_type, connector_length, [])
self.transitions.append(transition)
return transition
```

## Update a state

The following method is used to update a state:

```python
def update_state(state: State, new_name: str | None = None, new_display_name: str | None = None) -> bool:
```

When the name is updated, it must be checked if the new name already exists for another state. If it does, the state is not updated and `False` is returned.

```python
if any(other_state.name == new_name and other_state != state for other_state in self.states):
    return False
```

If the new name does not exist yet, it is updated for the state and the name of the source and target states of all transitions that have the state as source or target are updated as well:

```python
if new_name is not None:
    for transition in self.transitions:
        if transition.source_name == state.name:
            transition.source_name = new_name
        elif transition.target_name == state.name:
            transition.target_name = new_name
    state.name = new_name
```

When the display name is updated, it is only updated for the state:

```python
if new_display_name is not None:
    state.display_name = new_display_name
```

Finally, `True` is returned to indicate that the state was updated successfully.

```python
return True
```

## Update a choice-point

The following method is used to update a choice-point:

```python
def update_choice_point(choice_point: ChoicePoint, new_name: str | None = None, new_question: str | None = None) -> bool:
```

When the name is updated, it must be checked if the new name already exists for another choice-point. If it does, the choice-point is not updated and `False` is returned.

```python
if any(other_choice_point.name == new_name and other_choice_point != choice_point for other_choice_point in self.choice_points):
    return False
```

If the new name does not exist yet, it is updated for the choice-point and the name of the source state of all transitions that have the choice-point as source is updated as well:

```python
if new_name is not None:
    for transition in self.transitions:
        if transition.source_name == choice_point.name:
            transition.source_name = new_name
    choice_point.name = new_name
```

When the question is updated, it is only updated for the choice-point:

```python
if new_question is not None:
    choice_point.question = new_question
```

Finally, `True` is returned to indicate that the choice-point was updated successfully.

```python
return True
```

## Update a transition

The following method is used to update a transition:

```python
def update_transition(transition: Transition, new_connector_type: str | None = None, new_connector_length: int | None = None, new_messages: List[Message] | None = None) -> bool:
```

The transition is updated by updating the connector type, length and/or messages.

```python
if new_connector_type is not None:
    transition.connector_type = new_connector_type
if new_connector_length is not None:
    transition.connector_length = new_connector_length
if new_messages is not None:
    transition.messages = new_messages
```

Finally, `True` is returned to indicate that the transition was updated successfully.

```python
return True
```

## Select an element

The following method is used to select an element:

```python
def select_element(element: Element) -> None:
```

This will update the `selected_element_identifiers` list and the `selection_indication_diagram`.

```python
self.selected_element_identifiers.append(element.identifier)
self.selection_indication_diagram.update()
```

## Deselect an element

The following method is used to deselect an element:

```python
def deselect_element(element: Element) -> None:
```

This will remove the element from the `selected_element_identifiers` list and update the `selection_indication_diagram`.

```python
self.selected_element_identifiers.remove(element.identifier)
self.selection_indication_diagram.update()
```

## Get the selected elements

The following method is used to get the selected elements:

```python
def get_selected_elements() -> List[Element]:
```

This will return the list of selected elements.

```python
return [self.get_element_by_identifier(identifier) for identifier in self.selected_element_identifiers]
```

## Deselect all elements

The following method is used to deselect all elements:  

```python
def deselect_all_elements() -> None:
```

This will clear the `selected_element_identifiers` list and update the `selection_indication_diagram`.

```python
self.selected_element_identifiers = []
self.selection_indication_diagram.update()
```

## Delete elements

The following method is used to delete elements from the diagram:

```python
def delete_elements(elements: List[Element]) -> None:
```

Removing the elements is done by iterating over the elements and using the `element_type` attribute to determine which list to remove the element from.

```python
for element in elements:
    match element.element_type:
        case ElementType.INTERFACE:
            self.delete_interface(element)
        case ElementType.MESSAGE:
            self.delete_message(element)
        case ElementType.STATE:
        self.delete_state(element)
        case ElementType.CHOICE_POINT:
            self.delete_choice_point(element)
        case ElementType.TRANSITION:
            self.delete_transition(element)
```

## Delete an interface

The following method is used to delete an interface:

```python
def delete_interface(interface: Interface) -> None:
```

The interface is removed from the `interfaces` list.

```python
self.interfaces.remove(interface)
```

The messages that have the interface as their `interface_name` are removed from the `messages` list.

```python
for message in self.messages:
    if message.interface_name == interface.name:
        self.delete_message(message)
```

## Delete a message

The following method is used to delete a message:

```python
def delete_message(message: Message) -> None:
```

The message is removed from the `messages` list.

```python
self.messages.remove(message)
```

Also, the message is removed from the `transitions` list of all transitions that have the message as one of their `messages`. Note that this is done by checking if the message's variable name is in the `messages` list of the transition.

```python
for transition in self.transitions:
    if message.get_variable_name() in transition.messages:
        transition.messages.remove(message)
```

## Delete a state

The following method is used to delete a state:

```python
def delete_state(state: State) -> None:
```

The state is removed from the `states` list.

```python
self.states.remove(state)
```

The transitions that have the state as their `source_name` or `target_name` are removed from the `transitions` list.

```python
for transition in self.transitions:
    if transition.source_name == state.name or transition.target_name == state.name:
        self.delete_transition(transition)
```

## Delete a choice-point

The following method is used to delete a choice-point:

```python
def delete_choice_point(choice_point: ChoicePoint) -> None:
```

The choice-point is removed from the `choice_points` list.

```python
self.choice_points.remove(choice_point)
```

The transitions that have the choice-point as their `source_name` are removed from the `transitions` list.

```python
for transition in self.transitions:
    if transition.source_name == choice_point.name:
        self.delete_transition(transition)
```

## Delete a transition

The following method is used to delete a transition:

```python
def delete_transition(transition: Transition) -> None:
```

The transition is removed from the `transitions` list.

```python
self.transitions.remove(transition)
```

## Add a new entry to the history

The following method is used to add a new entry to the history:

```python
def add_history(plantuml_code: str) -> None:
```

The `plantuml_code` is added to the `history` list and the `current_history_index` is incremented. Also, any future entries in the history are removed.

```python
self.history.append(plantuml_code)
self.current_history_index += 1
self.history = self.history[:self.current_history_index]
```

## Undo the last action

The following method is used to undo the last action:

```python
def undo() -> str | None:
```

If the `current_index` is 0, which means that there are no previous actions in the history, `None` is returned.

```python
if self.current_history_index == 0:
    return None
```

The `current_history_index` is decremented and the PlantUML code at the new `current_history_index` is returned.

```python
self.current_history_index -= 1
return self.history[self.current_history_index]
```

## Redo the last action

The following method is used to redo the last action:

```python
def redo() -> str | None:
```

If the `current_history_index` is equal to the length of the history, which means that there are no future actions in the history, `None` is returned.

```python
if self.current_history_index == len(self.history):
    return None
```

The `current_history_index` is incremented and the PlantUML code at the new `current_history_index` is returned.

```python
self.current_history_index += 1
return self.history[self.current_history_index]
```

## Get PlantUML code

To generate a complete PlantUML code, the following method is used which returns the PlantUML code of the diagram, depending on the type of the code.

```python
get_plantuml_code(code_type: CodeType) -> str
```

The first step is to add the header code and the default messages code:

```python
plantuml_code = HEADER_PLANTUML_CODE + DEFAULT_MESSAGES_PLANTUML_CODE
```

The next step is to add the PlantUML code for the interfaces, messages, component, states, choice-points and transitions:

```python
plantuml_code += get_interfaces_plantuml_code()
plantuml_code += get_messages_plantuml_code()
plantuml_code += get_component_plantuml_code(code_type)
plantuml_code += get_states_plantuml_code(code_type)
plantuml_code += get_choice_points_plantuml_code(code_type)
plantuml_code += get_transitions_plantuml_code(code_type)
```

Finally, the footer code is added and the complete PlantUML code is returned:

```python
plantuml_code += FOOTER_PLANTUML_CODE
return plantuml_code
```

## Get interfaces PlantUML code

The `get_interfaces_plantuml_code()` method returns the PlantUML code for the interfaces.

```python
get_interfaces_plantuml_code() -> str
```

First the section for the interfaces is created:

```python
plantuml_code = INTERFACES_PLANTUML_CODE
```

The code is generated by iterating over all interfaces and adding the PlantUML code for each interface. After this, the string is returned:

```python
for interface in interfaces:
    plantuml_code += f"{interface.get_plantuml_code()}\n"
return plantuml_code
```

## Get messages PlantUML code

The `get_messages_plantuml_code()` method returns the PlantUML code for the messages.

```python
get_messages_plantuml_code() -> str
```

First the section for the messages is created:

```python
plantuml_code = MESSAGES_PLANTUML_CODE
```

The code is generated by iterating over all messages and adding the PlantUML code for each message. After this, the string is returned:

```python
for message in messages:
    plantuml_code += f"{message.get_plantuml_code()}\n"
return plantuml_code
```

## Get component PlantUML code

The `get_component_plantuml_code()` method returns the PlantUML code for the component, depending on the type of the code.

```python
get_component_plantuml_code(code_type: CodeType) -> str
```

First the section for the component is created:

```python
plantuml_code = COMPONENT_PLANTUML_CODE
```

This section contains the `START` state. When this state is selected, the element must be colored red. Otherwise, the element must be colored black. Since the `START` state has the identifier `0`, this is used to check if the state is selected.

```python
if code_type == CodeType.SELECTED and 0 in selected_element_identifiers:
    plantuml_code += "#FF0000\n"
else:
    plantuml_code += "#000000\n"
```

After this, the string is returned:

```python
return plantuml_code
```

## Get states PlantUML code

The `get_states_plantuml_code()` method returns the PlantUML code for the states, depending on the type of the code.

```python
get_states_plantuml_code(code_type: CodeType) -> str
```

First the section for the states is created:

```python
plantuml_code = STATES_PLANTUML_CODE
```

The code is generated by iterating over all states and adding the PlantUML code for each state. This is done by checking whether the code type is `CodeType.SELECTED` and whether the state is selected which can be checked by checking if the state's identifier is in the `selected_element_identifiers` list. After this, the string is returned:

```python
for state in states:
    state_code_type = CodeType.SELECTED if code_type == CodeType.SELECTED and state.identifier in selected_element_identifiers else CodeType.STANDARD
    plantuml_code += f"{state.get_plantuml_code(state_code_type)}\n"
return plantuml_code
```

## Get choice-points PlantUML code

The `get_choice_points_plantuml_code()` method returns the PlantUML code for the choice-points, depending on the type of the code.

```python
get_choice_points_plantuml_code(code_type: CodeType) -> str
```

First the section for the choice-points is created:

```python
plantuml_code = CHOICE_POINTS_PLANTUML_CODE
```

The code is generated by iterating over all choice-points and adding the PlantUML code for each choice-point. This is done by checking whether the code type is `CodeType.SELECTED` and whether the choice-point is selected which can be checked by checking if the choice-point's identifier is in the `selected_element_identifiers` list. After this, the string is returned:

```python
for choice_point in choice_points:
    choice_point_code_type = CodeType.SELECTED if code_type == CodeType.SELECTED and choice_point.identifier in selected_element_identifiers else CodeType.STANDARD
    plantuml_code += f"{choice_point.get_plantuml_code(choice_point_code_type)}\n"
return plantuml_code
```

## Get transitions PlantUML code

The `get_transitions_plantuml_code()` method returns the PlantUML code for the transitions, depending on the type of the code.

```python
get_transitions_plantuml_code(code_type: CodeType) -> str
```

First the section for the transitions is created:

```python
plantuml_code = TRANSITIONS_PLANTUML_CODE
```

The code is generated by iterating over all transitions and adding the PlantUML code for each transition. This is done by checking whether the code type is `CodeType.SELECTED` and whether the transition is selected which can be checked by checking if the transition's identifier is in the `selected_element_identifiers` list. After this, the string is returned:

```python
for transition in transitions:
    transition_code_type = CodeType.SELECTED if code_type == CodeType.SELECTED and transition.identifier in selected_element_identifiers else CodeType.STANDARD
    plantuml_code += f"{transition.get_plantuml_code(transition_code_type)}\n"
return plantuml_code
``` 
