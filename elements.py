from enum import Enum
import re
from typing import Optional, List

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

class CodeType(Enum):
    STANDARD = "Standard"
    SELECTED = "Selected"
    MASKED = "Masked"

# Base class
class Element:
    def __init__(self, element_type: ElementType, identifier: int):
        self.element_type = element_type
        self.identifier = identifier

    def get_plantuml_code(self, code_type: CodeType = CodeType.STANDARD) -> str:
        raise NotImplementedError

    def get_variable_name(self) -> str:
        raise NotImplementedError

    @classmethod
    def from_plantuml_code(cls, plantuml_code: str):
        raise NotImplementedError

# Interface class
class Interface(Element):
    def __init__(self, identifier: int, name: str):
        super().__init__(ElementType.INTERFACE, identifier)
        self.name = name

    def get_plantuml_code(self, code_type: CodeType = CodeType.STANDARD) -> str:
        return f"!{self.get_variable_name()} = {self.name}"

    def get_variable_name(self) -> str:
        return f"${self.name}"

    @classmethod
    def from_plantuml_code(cls, plantuml_code: str):
        name = plantuml_code.split("=")[1].strip()
        identifier = 0
        return cls(identifier, name)

# Message class
class Message(Element):
    def __init__(self, identifier: int, name: str, interface: Optional[str] = None):
        super().__init__(ElementType.MESSAGE, identifier)
        self.name = name
        self.interface = interface

    def get_plantuml_code(self, code_type: CodeType = CodeType.STANDARD) -> str:
        return f"!{self.get_variable_name()} = {self.interface} + \":\" + {self.name}"

    def get_variable_name(self) -> str:
        if self.interface:
            return f"{self.interface}_{self.name}"
        return f"${self.name}"

    @classmethod
    def from_plantuml_code(cls, plantuml_code: str):
        name = plantuml_code[plantuml_code.rfind("+") + 1:].strip()
        interface = plantuml_code[:plantuml_code.rfind("+")].strip()
        identifier = 0
        return cls(identifier, name, interface)

# State class
class State(Element):
    def __init__(self, identifier: int, name: str, display_name: Optional[str] = None):
        super().__init__(ElementType.STATE, identifier)
        self.name = name
        self.display_name = display_name

    def get_plantuml_code(self, code_type: CodeType = CodeType.STANDARD) -> str:
        standard_code = f"state {self.get_variable_name()}"
        if self.display_name:
            standard_code = f"{standard_code} as \"{self.display_name}\""
        match code_type:
            case CodeType.STANDARD:
                return standard_code
            case CodeType.SELECTED:
                return f"{standard_code} #line:FF0000;line.bold"
            case CodeType.MASKED:
                return f"{standard_code} #0000{self.identifier:02X};line:0000{self.identifier:02X}"

    def get_variable_name(self) -> str:
        return f"{self.name}"

    @classmethod
    def from_plantuml_code(cls, plantuml_code: str):
        match = re.search(r'state\s+(\w+)', plantuml_code)
        name = match.group(1) if match else None
        display_match = re.search(r'as\s+"([^"]+)"', plantuml_code)
        display_name = display_match.group(1) if display_match else None
        identifier = 0
        return cls(identifier, name, display_name)

# ChoicePoint class
class ChoicePoint(Element):
    def __init__(self, identifier: int, name: str, question: str):
        super().__init__(ElementType.CHOICE_POINT, identifier)
        self.name = name
        self.question = question

    def get_plantuml_code(self, code_type: CodeType = CodeType.STANDARD) -> str:
        if not self.question.endswith("?"):
            self.question += "?"
        standard_code = f"state {self.get_variable_name()} as \"{self.question}\""
        match code_type:
            case CodeType.STANDARD:
                return standard_code
            case CodeType.SELECTED:
                return f"{standard_code} #line:FF0000;line.bold"
            case CodeType.MASKED:
                return f"{standard_code} #0000{self.identifier:02X};line:0000{self.identifier:02X}"

    def get_variable_name(self) -> str:
        return f"CP_{self.name}"

    @classmethod
    def from_plantuml_code(cls, plantuml_code: str):
        match = re.search(r'state\s+(\w+)', plantuml_code)
        name = match.group(1)[3:] if match else None
        question = plantuml_code[plantuml_code.find("as") + 3:plantuml_code.find('"')].strip()
        identifier = 0
        return cls(identifier, name, question)

# Transition class
class Transition(Element):
    def __init__(self, identifier: int, source_state: str, target_state: str, connector_type: ConnectorType, connector_length: int, messages: Optional[List[str]] = None):
        super().__init__(ElementType.TRANSITION, identifier)
        self.source_state = source_state
        self.target_state = target_state
        self.connector_type = connector_type
        self.connector_length = connector_length
        self.messages = messages if messages is not None else []

    def get_plantuml_code(self, code_type: CodeType = CodeType.STANDARD) -> str:
        arrow_code_type = ""
        match code_type:
            case CodeType.STANDARD:
                arrow_code_type = ""
            case CodeType.SELECTED:
                arrow_code_type = "[#FF0000,bold]"
            case CodeType.MASKED:
                arrow_code_type = f"[#0000{self.identifier:02X},0000{self.identifier:02X},thickness=8]"

        connector_code = ""
        match self.connector_type:
            case ConnectorType.LEFT:
                connector_code = f"-left{arrow_code_type}->"
            case ConnectorType.RIGHT:
                connector_code = f"-{arrow_code_type}>"
            case ConnectorType.UP:
                connector_code = f"-up{arrow_code_type}->"
            case ConnectorType.DOWN:
                connector_code = f"-{arrow_code_type}->"

        if self.connector_type in [ConnectorType.UP, ConnectorType.DOWN]:
            for _ in range(self.connector_length - 1):
                connector_code += "-"

        transition_code = f"{self.source_state} {connector_code} {self.target_state}"

        if len(self.messages) > 0:
            transition_code += " : "
            for message in self.messages:
                transition_code += f"{message}\\n"
        return transition_code

    def get_variable_name(self) -> str:
        pass

    @classmethod
    def from_plantuml_code(cls, plantuml_code: str):
        parts = plantuml_code.split()
        source_state = parts[0]
        connector = parts[1]
        connector_type = ConnectorType.UP if "-up" in connector else ConnectorType.RIGHT if "-right" in connector else ConnectorType.DOWN if "--" in connector else ConnectorType.LEFT
        connector_length = connector.count("-") - 1 if connector_type in [ConnectorType.UP, ConnectorType.DOWN] else 1
        target_state = parts[2]
        messages_list = parts[4:]
        messages = [message.strip() for message in messages_list]
        identifier = 0
        return cls(identifier, source_state, target_state, connector_type, connector_length, messages)
