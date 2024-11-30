from enum import Enum
from typing import List

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

class Element:
    def __init__(self, element_type: ElementType, identifier: int):
        self.element_type = element_type
        self.identifier = identifier

class Interface(Element):
    def __init__(self, identifier: int, name: str):
        super().__init__(ElementType.INTERFACE, identifier)
        self.name = name

class Message(Element):
    def __init__(self, identifier: int, name: str, interface: str):
        super().__init__(ElementType.MESSAGE, identifier)
        self.name = name
        self.interface = interface

class State(Element):
    def __init__(self, identifier: int, name: str, display_name: str):
        super().__init__(ElementType.STATE, identifier)
        self.name = name
        self.display_name = display_name

class ChoicePoint(Element):
    def __init__(self, identifier: int, name: str, question: str):
        super().__init__(ElementType.CHOICE_POINT, identifier)
        self.name = name
        self.question = question

class Transition(Element):
    def __init__(self, identifier: int, source_state: State, target_state: State, 
                 connector_type: ConnectorType, connector_length: int, messages: List[Message]):
        super().__init__(ElementType.TRANSITION, identifier)
        self.source_state = source_state
        self.target_state = target_state
        self.connector_type = connector_type
        self.connector_length = connector_length
        self.messages = messages
