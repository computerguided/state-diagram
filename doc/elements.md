# Elements

_This module contains the classes representing the elements of the diagram._

## Enums

The following enums are defined:

- `ElementType`: an enum containing the types of the elements.
- `ConnectorType`: an enum containing the types of the connectors.

The `ElementType` enum is defined as follows:

```python
class ElementType(Enum):
    INTERFACE = "Interface"
    MESSAGE = "Message"
    STATE = "State"
    CHOICE_POINT = "ChoicePoint"
    TRANSITION = "Transition"
```

The `ConnectorType` enum is defined as follows:

```python
class ConnectorType(Enum):
    LEFT = "Left"
    RIGHT = "Right"
    UP = "Up"
    DOWN = "Down"
```

## Element base class

The `Element` class is the base class for all elements in the diagram.

It has the following attributes:

- `element_type`: an enum containing the type of the element (e.g. `Interface`, `Message`, `State`, `ChoicePoint`, or `Transition`).
- `identifier`: an integer containing the identifier of the element.

## Constructor

The constructor of the class takes no arguments.

```python
def __init__(self, element_type: ElementType, identifier: int):
```

## Methods

The class has the following methods:

- `get_plantuml_code()`: returns the PlantUML code of the element. This is overridden by the subclasses.
- `get_variable_name()`: returns the variable name of the element. This is overridden by the subclasses.

## Interface

The `Interface` class is a subclass of `Element` with the type set to `Interface` and is responsible for holding the data of an interface. It has the following additional attributes:

- `name`: a string containing the name of the interface.

## Constructor

The constructor of the class takes the following arguments:

```python
    def __init__(self, identifier: int, name: str):
        super().__init__(ElementType.INTERFACE, identifier)
        self.name = name
```

## Methods

The class has the following methods:

- [`get_plantuml_code()`](#get-interface-plantuml-code): returns the PlantUML code of the interface.
- [`get_variable_name()`](#get-interface-variable-name): returns the variable name of the interface.

## Get interface PlantUML code

An interface is represented by a variable in the PlantUML code for example:

```
!$RTx = RTx
```

To generate this code the following method is used:

```python
def get_plantuml_code(self) -> str:
```

The method returns the PlantUML code of the interface which is specified as follows:
```python
return f"!{self.get_variable_name()} = {self.name}"
```

## Get interface variable name

For an interface the variable name is `$<name>`. This is generated by the following method:

```python
def get_variable_name(self) -> str:
    return f"${self.name}"
```

## Message

The `Message` class is a subclass of `Element` with the type set to `Message` and is responsible for holding the data of a message. It has the following additional attributes:

- `name`: a string containing the name of the message.
- `interface`: a string containing the name of the interface of the message.

## Constructor

The constructor of the class takes the following arguments:

```python
    def __init__(self, identifier: int, name: str, interface: Interface):
        super().__init__(ElementType.MESSAGE, identifier)
        self.name = name
        self.interface = interface
```

## Methods

The class has the following methods:

- [`get_plantuml_code()`](#get-message-plantuml-code): returns the PlantUML code of the message.
- [`get_variable_name()`](#get-message-variable-name): returns the variable name of the message.

## Get message PlantUML code

A message is represented by a variable in the PlantUML code for example:

```
!$RTx_ConnectReq = $RTx + ":" + ConnectReq
```

To generate this code the following method is used:

```python
def get_plantuml_code(self) -> str:
```

The method returns the PlantUML code of the message which is specified as follows:

```python
return f"!{self.get_variable_name()} = {self.interface.get_variable_name()} + \":\" + {self.name}"
```

## Get message variable name

A message is represented by a variable in the PlantUML code for example:

```
$RTx_ConnectReq
```

For a message the variable name is `$<interface>_<name>`. This is generated by the following method:

```python
def get_variable_name(self) -> str:
    return f"{self.interface.get_variable_name()}_{self.name}"
```

## State

The `State` class is a subclass of `Element` with the type set to `State` and is responsible for holding the data of a state. It has the following additional attributes:

- `name`: a string containing the name of the state.
- `display_name`: a string containing the display name of the state.

## Constructor

The constructor of the class takes the following arguments:

```python
    def __init__(self, identifier: int, name: str, display_name: str | None = None):
        super().__init__(ElementType.STATE, identifier)
        self.name = name
        self.display_name = display_name
```

## Methods

The class has the following methods:

- [`get_plantuml_code()`](#get-state-plantuml-code): returns the PlantUML code of the state.
- [`get_variable_name()`](#get-state-variable-name): returns the variable name of the state.

## Get state PlantUML code

A state is represented by a variable in the PlantUML code for example:

```
state Connecting
```

To generate this code the following method is used:

```python
def get_plantuml_code(self) -> str:
```

The method returns the PlantUML code of the state which is specified - depending on whether the display name is `None` or not - as follows:

```python
if self.display_name is None:
    return f"state {self.get_variable_name()}"
else:
    return f"state {self.get_variable_name()} as \"{self.display_name}\""
```

## Get state variable name

For a state the variable name is simply the name of the state. This is generated by the following method:

```python
def get_variable_name(self) -> str:
    return f"{self.name}"
```

## Choice-point

The `ChoicePoint` class is a subclass of `Element` with the type set to `ChoicePoint` and is responsible for holding the data of a choice-point. It has the following additional attributes:

- `name`: a string containing the name of the choice-point.
- `question`: a string containing the question of the choice-point.

## Constructor

The constructor of the class takes the following arguments:

```python
    def __init__(self, identifier: int, name: str, question: str):
        super().__init__(ElementType.CHOICE_POINT, identifier)
        self.name = name
        self.question = question
```

## Methods

The class has the following methods:

- [`get_plantuml_code()`](#get-choice-point-plantuml-code): returns the PlantUML code of the choice-point.
- [`get_variable_name()`](#get-choice-point-variable-name): returns the variable name of the choice-point.

## Get choice-point PlantUML code

A choice-point is represented by a variable in the PlantUML code for example:

```
state CP_Whitelisted as "Is Server\nWhitelisted?"
```

To generate this code the following method is used:

```python
def get_plantuml_code(self) -> str:
```

The method returns the PlantUML code of the choice-point. It also checks whether the `question` ends with a question mark and adds this when this is not the case. It then returns the appropriate code:

```python
if self.question.endswith("?"):
    return f"state {self.get_variable_name()} as \"{self.question}\""
else:
    return f"state {self.get_variable_name()} as \"{self.question}?\""
```

## Get choice-point variable name

For a choice-point the variable name is `CP_<name>`. This is generated by the following method:

```python
def get_variable_name(self) -> str:
    return f"CP_{self.name}"
```

## Transition

The `Transition` class is a subclass of `Element` with the type set to `Transition` and is responsible for holding the data of a transition. It has the following additional attributes:

- `source_state`: a `State` object containing the source state of the transition.
- `target_state`: a `State` object containing the target state of the transition.
- `connector_type`: an enum (`Left`, `Right`, `Up`, `Down`) containing the type of the connector of the transition.
- `connector_length`: an integer containing the length of the connector of the transition.
- `messages`: a list of `Message` objects containing the messages of the transition.

## Constructor

The constructor of the class takes the following arguments of which the messages is optional because it can be empty.

```python
    def __init__(self, identifier: int, source_state: State, target_state: State, connector_type: ConnectorType, connector_length: int, messages: list[Message] | None = None):
        super().__init__(ElementType.TRANSITION, identifier)
        self.source_state = source_state
        self.target_state = target_state
        self.connector_type = connector_type
        self.connector_length = connector_length
        self.messages = messages if messages is not None else []
```

## Methods

The class has the following methods:

- [`get_plantuml_code()`](#get-transition-plantuml-code): returns the PlantUML code of the transition.
- [`get_variable_name()`](#get-transition-variable-name): returns the variable name of the transition.

## Get transition PlantUML code

A transition is represented by a variable in the PlantUML code for example:

```
Connecting -> Advertising : $RTx_ConnectReq\n$RTx_ConnectedInd
```

To generate this code the following method is used:

```python
def get_plantuml_code(self) -> str:
```

The method returns the PlantUML code of the transition. This is less trivial because of the connector type and length.

As such first the connector type is checked and the appropriate code is generated.

```python
connector_code = ""
match self.connector_type:
    case ConnectorType.LEFT:
        connector_code = ""
    case ConnectorType.RIGHT:
        connector_code = "-[right]"
    case ConnectorType.UP:
        connector_code = "-[up]"
    case ConnectorType.DOWN:
        connector_code = "-"
```

With this set, it is checked whether the `connector_type` is `UP` or `DOWN`. If this is the case, the `connector_length` is checked. When this is greater that 1, additional `-` characters are added to the connector code.

```python
if self.connector_type in [ConnectorType.UP, ConnectorType.DOWN]:
    for _ in range(self.connector_length - 1):
        connector_code += "-"
```

Next the first part of the transition can be generated by adding the source state, the connector code with the `->` and the target state.

```python
transition_code = f"{self.source_state.name} {connector_code}-> {self.target_state.name}"
```

Finally the messages are added to the transition code. This is only done if there are any messages. If that is the case, first a `:` is added and then the messages separated by a new line character.

```python
if len(self.messages) > 0:
    transition_code += f" : {'\n'.join([message.get_variable_name() for message in self.messages])}"
```

## Get transition variable name

For a transition the variable name is not used and is not generated. To prevent an error the following method is defined but does nothing.

```python
def get_variable_name(self) -> str:
    pass
```