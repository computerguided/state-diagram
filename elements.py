from enum import Enum
from typing import List, Optional

# Enums
class ElementType(Enum):
    INTERFACE = "Interface"
    MESSAGE = "Message"
    STATE = "State"
    CHOICE_POINT = "ChoicePoint"
    TRANSITION = "Transition"

class ConnectorType(Enum):
    LEFT = "Left"
    RIGHT = "Right"
    UP = "Up"
    DOWN = "Down"

# Element base class
class Element:
    def __init__(self, element_type: ElementType, identifier: int):
        self.element_type = element_type
        self.identifier = identifier

    def get_plantuml_code(self) -> str:
        raise NotImplementedError("Subclasses should implement this method.")

    def get_variable_name(self) -> str:
        raise NotImplementedError("Subclasses should implement this method.")

# Interface class
class Interface(Element):
    def __init__(self, identifier: int, name: str):
        super().__init__(ElementType.INTERFACE, identifier)
        self.name = name

    def get_plantuml_code(self) -> str:
        return f"!{self.get_variable_name()} = {self.name}"

    def get_variable_name(self) -> str:
        return f"${self.name}"

# Message class
class Message(Element):
    def __init__(self, identifier: int, name: str, interface: Interface):
        super().__init__(ElementType.MESSAGE, identifier)
        self.name = name
        self.interface = interface

    def get_plantuml_code(self) -> str:
        return f"!{self.get_variable_name()} = {self.interface.get_variable_name()} + \":\" + {self.name}"

    def get_variable_name(self) -> str:
        return f"{self.interface.get_variable_name()}_{self.name}"

# State class
class State(Element):
    def __init__(self, identifier: int, name: str, display_name: Optional[str] = None):
        super().__init__(ElementType.STATE, identifier)
        self.name = name
        self.display_name = display_name

    def get_plantuml_code(self) -> str:
        if self.display_name is None:
            return f"state {self.get_variable_name()}"
        else:
            return f"state {self.get_variable_name()} as \"{self.display_name}\""

    def get_variable_name(self) -> str:
        return f"{self.name}"

# ChoicePoint class
class ChoicePoint(Element):
    def __init__(self, identifier: int, name: str, question: str):
        super().__init__(ElementType.CHOICE_POINT, identifier)
        self.name = name
        self.question = question

    def get_plantuml_code(self) -> str:
        if self.question.endswith("?"):
            return f"state {self.get_variable_name()} as \"{self.question}\""
        else:
            return f"state {self.get_variable_name()} as \"{self.question}?\""

    def get_variable_name(self) -> str:
        return f"CP_{self.name}"

# Transition class
class Transition(Element):
    def __init__(self, identifier: int, source_state: State, target_state: State, connector_type: ConnectorType, connector_length: int, messages: Optional[List[Message]] = None):
        super().__init__(ElementType.TRANSITION, identifier)
        self.source_state = source_state
        self.target_state = target_state
        self.connector_type = connector_type
        self.connector_length = connector_length
        self.messages = messages if messages is not None else []

    def get_plantuml_code(self) -> str:
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

        if self.connector_type in [ConnectorType.UP, ConnectorType.DOWN]:
            for _ in range(self.connector_length - 1):
                connector_code += "-"

        transition_code = f"{self.source_state.get_variable_name()} {connector_code}-> {self.target_state.get_variable_name()}"

        if len(self.messages) > 0:
            transition_code += f" : {'\n'.join([message.get_variable_name() for message in self.messages])}"

        return transition_code

    def get_variable_name(self) -> str:
        pass
