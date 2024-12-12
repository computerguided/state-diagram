from diagram import Diagram
from elements import Interface, Message, State, ChoicePoint, Transition, CodeType, ElementType, ConnectorType

from enum import Enum
import atexit
import subprocess
import time

# --------------------------------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------------------------------

PLANTUML_PORT = 9000

SECTION_START_INDICATOR = "'== "
SECTION_END_INDICATOR = " =="

# --------------------------------------------------------------------------------------------------
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

# --------------------------------------------------------------------------------------------------
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

# --------------------------------------------------------------------------------------------------
DEFAULT_INTERFACES_PLANTUML_CODE = """'== Default interfaces ==
!$Logical = Logical
!$Timer = Timer
"""

# --------------------------------------------------------------------------------------------------
DEFAULT_MESSAGES_PLANTUML_CODE = """
'== Default messages ==
!$Timer_Timeout = Timeout
!$Logical_No = No
!$Logical_Yes = Yes
"""

# --------------------------------------------------------------------------------------------------
INTERFACES_PLANTUML_CODE = """'== Interfaces ==
"""

# --------------------------------------------------------------------------------------------------
MESSAGES_PLANTUML_CODE = """'== Messages ==
"""

# --------------------------------------------------------------------------------------------------
COMPONENT_PLANTUML_CODE = """'== Component ==
"""

# --------------------------------------------------------------------------------------------------
STATES_PLANTUML_CODE = """'== States ==
"""

# --------------------------------------------------------------------------------------------------
CHOICE_POINTS_PLANTUML_CODE = """'== Choice-points ==
"""

# --------------------------------------------------------------------------------------------------
TRANSITIONS_PLANTUML_CODE = """'== Transitions ==
"""

# --------------------------------------------------------------------------------------------------
FOOTER_PLANTUML_CODE = """'== Footer ==
}
@enduml"""

# --------------------------------------------------------------------------------------------------
SECTIONS = [HEADER_PLANTUML_CODE, DEFAULT_INTERFACES_PLANTUML_CODE, DEFAULT_MESSAGES_PLANTUML_CODE, INTERFACES_PLANTUML_CODE, MESSAGES_PLANTUML_CODE, COMPONENT_PLANTUML_CODE, STATES_PLANTUML_CODE, CHOICE_POINTS_PLANTUML_CODE, TRANSITIONS_PLANTUML_CODE, FOOTER_PLANTUML_CODE]

# --------------------------------------------------------------------------------------------------
# Enums
# --------------------------------------------------------------------------------------------------

class EditActionType(Enum):
    NON_VISUAL = "non_visual"
    VISUAL = "visual"
    SELECTION = "selection"

# --------------------------------------------------------------------------------------------------
# PlantUMLManager
# --------------------------------------------------------------------------------------------------

class PlantUMLManager:

    # ----------------------------------------------------------------------------------------------
    # Constructor
    # ----------------------------------------------------------------------------------------------

    def __init__(self):

        self.process = self.start_plantuml_server(PLANTUML_PORT)
        self.plantuml_endpoint = f"http://localhost:{PLANTUML_PORT}/png/"

        self.component_name = "Component Name"

        self.state_diagram = Diagram(self.plantuml_endpoint)
        self.selection_mask_diagram = Diagram(self.plantuml_endpoint)
        self.selection_indication_diagram = Diagram(self.plantuml_endpoint)

        self.interfaces = []
        self.messages = []
        self.states = []
        self.choice_points = []
        self.transitions = []
        self.elements = []
        self.selected_element_identifiers = []
        
        self.history = [self.get_plantuml_code(CodeType.STANDARD)]
        self.current_history_index = 0

    # ----------------------------------------------------------------------------------------------
    def start_plantuml_server(self, port: int) -> subprocess.Popen:
        command = ["java", "-jar", "plantuml.jar", f"-picoweb:{port}"]
        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)
        atexit.register(self.cleanup)
        return process
    
    # ----------------------------------------------------------------------------------------------
    def cleanup(self):
        if self.process.poll():
            return
        self.process.terminate()
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.kill()

    # ----------------------------------------------------------------------------------------------
    def set_elements(self, plantuml_code: str):
        self.interfaces.clear()
        self.messages.clear()
        self.states.clear()
        self.choice_points.clear()
        self.transitions.clear()
        self.elements.clear()
        self.selected_element_identifiers.clear()

        previous_history = self.history.copy()
        previous_current_history_index = self.current_history_index

        self.add_default_interfaces()
        self.add_default_messages()
        self.add_default_states()

        self.history = previous_history
        self.current_history_index = previous_current_history_index

        self.states.append(State(0, "START"))
        self.interfaces += self.get_interfaces_from_plantuml_code(plantuml_code)
        self.messages += self.get_messages_from_plantuml_code(plantuml_code)
        self.component_name = self.get_component_from_plantuml_code(plantuml_code)
        self.states += self.get_states_from_plantuml_code(plantuml_code)
        self.choice_points += self.get_choice_points_from_plantuml_code(plantuml_code)
        self.transitions += self.get_transitions_from_plantuml_code(plantuml_code)
        self.elements = self.states + self.choice_points + self.transitions + self.interfaces + self.messages
        for i, element in enumerate(self.elements):
            element.identifier = i

    # ----------------------------------------------------------------------------------------------
    def add_default_interfaces(self):
        self.add_interface("Timer")
        self.add_interface("Logical")

    # ----------------------------------------------------------------------------------------------
    def add_default_messages(self):
        self.add_message("Timer", "Timeout")
        self.add_message("Logical", "No")
        self.add_message("Logical", "Yes")

    # ----------------------------------------------------------------------------------------------
    def add_default_states(self):
        self.add_state("START")

    # ----------------------------------------------------------------------------------------------
    def get_interfaces_from_plantuml_code(self, plantuml_code: str):
        interfaces_index = plantuml_code.find(INTERFACES_PLANTUML_CODE) + len(INTERFACES_PLANTUML_CODE)
        lines = []
        for line in plantuml_code[interfaces_index:].split("\n"):
            if line == "" or line.startswith(SECTION_START_INDICATOR):
                break
            lines.append(line)
        interfaces = []
        for line in lines:
            interface = Interface.from_plantuml_code(line)
            interfaces.append(interface)
        return interfaces

    # ----------------------------------------------------------------------------------------------
    def get_messages_from_plantuml_code(self, plantuml_code: str):
        messages_index = plantuml_code.find(MESSAGES_PLANTUML_CODE) + len(MESSAGES_PLANTUML_CODE)
        lines = []
        for line in plantuml_code[messages_index:].split("\n"):
            if line == "" or line.startswith(SECTION_START_INDICATOR):
                break
            lines.append(line)
        messages = []
        for line in lines:
            message = Message.from_plantuml_code(line)
            messages.append(message)
        return messages

    # ----------------------------------------------------------------------------------------------
    def get_component_from_plantuml_code(self, plantuml_code: str):
        component_index = plantuml_code.find(COMPONENT_PLANTUML_CODE)
        component_name_line = plantuml_code[component_index+len(COMPONENT_PLANTUML_CODE):].split("\n")[0]
        component_name = component_name_line.split('"')[1]
        return component_name


    def get_states_from_plantuml_code(self, plantuml_code: str):
        states_index = plantuml_code.find(STATES_PLANTUML_CODE) + len(STATES_PLANTUML_CODE)
        lines = []
        for line in plantuml_code[states_index:].split("\n"):
            if line == "" or line.startswith(SECTION_START_INDICATOR):
                break
            lines.append(line)
        states = []
        for line in lines:
            state = State.from_plantuml_code(line)
            states.append(state)
        return states

    # ----------------------------------------------------------------------------------------------
    def get_choice_points_from_plantuml_code(self, plantuml_code: str):
        choice_points_index = plantuml_code.find(CHOICE_POINTS_PLANTUML_CODE) + len(CHOICE_POINTS_PLANTUML_CODE)
        lines = []
        for line in plantuml_code[choice_points_index:].split("\n"):
            if line == "" or line.startswith(SECTION_START_INDICATOR):
                break
            lines.append(line)
        choice_points = []
        for line in lines:
            choice_point = ChoicePoint.from_plantuml_code(line)
            choice_points.append(choice_point)
        return choice_points

    # ----------------------------------------------------------------------------------------------
    def get_transitions_from_plantuml_code(self, plantuml_code: str):
        transitions_index = plantuml_code.find(TRANSITIONS_PLANTUML_CODE) + len(TRANSITIONS_PLANTUML_CODE)
        lines = []
        for line in plantuml_code[transitions_index:].split("\n"):
            if line == "" or line.startswith(SECTION_START_INDICATOR):
                break
            lines.append(line)
        transitions = []
        for line in lines:
            transition = Transition.from_plantuml_code(line)
            transitions.append(transition)
        return transitions

    # ----------------------------------------------------------------------------------------------
    def load_diagram(self, plantuml_code: str) -> bool:
        if not self.validate_plantuml_code(plantuml_code):
            return False
        self.set_elements(plantuml_code)
        if not self.state_diagram.set_plantuml_code(self.get_plantuml_code(CodeType.STANDARD)):
            return False
        if not self.selection_mask_diagram.set_plantuml_code(self.get_plantuml_code(CodeType.MASKED)):
            return False
        if not self.selection_indication_diagram.set_plantuml_code(self.get_plantuml_code(CodeType.SELECTED)):
            return False
        self.add_history(plantuml_code)
        return True
    
    # ----------------------------------------------------------------------------------------------
    def set_plantuml_code(self, plantuml_code: str):
        self.set_elements(plantuml_code)
        self.state_diagram.set_plantuml_code(self.get_plantuml_code(CodeType.STANDARD))
        self.selection_mask_diagram.set_plantuml_code(self.get_plantuml_code(CodeType.MASKED))
        self.selection_indication_diagram.set_plantuml_code(self.get_plantuml_code(CodeType.SELECTED))

    # ----------------------------------------------------------------------------------------------
    def validate_plantuml_code(self, plantuml_code: str) -> bool:
        diagram = Diagram(self.plantuml_endpoint)
        if not diagram.set_plantuml_code(plantuml_code):
            print("Diagram detected invalid PlantUML code!")
            return False
        previous_index = -1
        for section in SECTIONS:
            index = plantuml_code.find(section)
            if index == -1 or index < previous_index:
                print(f"Missing section {section} detected!")
                return False
            previous_index = index
        return True
    
    # ----------------------------------------------------------------------------------------------
    def update_diagrams(self, action: EditActionType):

        standard_plantuml_code = self.get_plantuml_code(CodeType.STANDARD)
        self.add_history(standard_plantuml_code)

        if action == EditActionType.NON_VISUAL:
            return
        
        plantuml_code = self.get_plantuml_code(CodeType.SELECTED)
        self.selection_indication_diagram.set_plantuml_code(plantuml_code)        

        if action == EditActionType.SELECTION or action == EditActionType.NON_VISUAL:
            return
        
        plantuml_code = self.get_plantuml_code(CodeType.STANDARD)
        self.state_diagram.set_plantuml_code(plantuml_code)
        plantuml_code = self.get_plantuml_code(CodeType.MASKED)
        self.selection_mask_diagram.set_plantuml_code(plantuml_code)

    # ----------------------------------------------------------------------------------------------
    def get_element_at(self, x: int, y: int):
        rgb_color = self.selection_mask_diagram.rendered_image.getpixel((x, y))
        if len(rgb_color) == 4:
            rgb_color = rgb_color[:3]
        index = rgb_color[0] * 256 * 256 + rgb_color[1] * 256 + rgb_color[2]
        return self.elements[index] if 0 <= index < len(self.elements) else None

    # ----------------------------------------------------------------------------------------------
    def add_interface(self, interface_name: str):
        if any(interface.name == interface_name for interface in self.interfaces):
            return None
        interface = Interface(len(self.elements), interface_name)
        self.interfaces.append(interface)
        self.elements.append(interface)
        self.update_diagrams(EditActionType.NON_VISUAL)
        return interface

    # ----------------------------------------------------------------------------------------------
    def add_message(self, interface_name: str, message_name: str):
        if any(message.interface == interface_name and message.name == message_name for message in self.messages):
            return None
        message = Message(len(self.elements), interface_name, message_name)
        self.messages.append(message)
        self.elements.append(message)
        self.update_diagrams(EditActionType.NON_VISUAL)
        return message

    # ----------------------------------------------------------------------------------------------
    def add_state(self, state_name: str, display_name: str = ""):
        if any(state.name == state_name for state in self.states):
            return None
        state = State(len(self.elements), state_name, display_name)
        self.states.append(state)
        self.elements.append(state)
        self.update_diagrams(EditActionType.VISUAL)
        return state

    # ----------------------------------------------------------------------------------------------
    def add_choice_point(self, choice_point_name: str, question: str = ""):
        if any(choice_point.name == choice_point_name for choice_point in self.choice_points):
            return None
        choice_point = ChoicePoint(len(self.elements), choice_point_name, question)
        self.choice_points.append(choice_point)
        self.elements.append(choice_point)
        self.update_diagrams(EditActionType.VISUAL)
        return choice_point

    # ----------------------------------------------------------------------------------------------
    def add_transition(self, source_name: str, target_name: str, connector_type: ConnectorType = ConnectorType.LEFT, connector_length: int = 1, messages: list = []):
        transition = Transition(len(self.elements), source_name, target_name, connector_type, connector_length, messages)
        self.transitions.append(transition)
        self.elements.append(transition)
        self.update_diagrams(EditActionType.VISUAL)
        return transition

    # ----------------------------------------------------------------------------------------------
    def update_state(self, state: State, new_name: str = None, new_display_name: str = None) -> bool:
        if any(other_state.name == new_name and other_state != state for other_state in self.states):
            return False
        if new_name is not None:
            for transition in self.transitions:
                if transition.source_name == state.name:
                    transition.source_name = new_name
                elif transition.target_name == state.name:
                    transition.target_name = new_name
            state.name = new_name
        if new_display_name is not None:
            state.display_name = new_display_name
        self.update_diagrams(EditActionType.VISUAL)
        return True

    # ----------------------------------------------------------------------------------------------
    def update_choice_point(self, choice_point: ChoicePoint, new_name: str = None, new_question: str = None) -> bool:
        if any(other_choice_point.name == new_name and other_choice_point != choice_point for other_choice_point in self.choice_points):
            return False
        if new_name is not None:
            for transition in self.transitions:
                if transition.source_name == choice_point.name:
                    transition.source_name = new_name
            choice_point.name = new_name
        if new_question is not None:
            choice_point.question = new_question
        self.update_diagrams(EditActionType.VISUAL)
        return True

    # ----------------------------------------------------------------------------------------------
    def update_transition(self, transition: Transition, new_connector_type: str = None, new_connector_length: int = None, new_messages: list = None) -> bool:
        if new_connector_type is not None:
            transition.connector_type = new_connector_type
        if new_connector_length is not None:
            transition.connector_length = new_connector_length
        if new_messages is not None:
            transition.messages = new_messages
        self.update_diagrams(EditActionType.VISUAL)
        return True

    # ----------------------------------------------------------------------------------------------
    def select_element(self, element):
        self.selected_element_identifiers.append(element.identifier)
        self.update_diagrams(EditActionType.SELECTION)

    # ----------------------------------------------------------------------------------------------
    def deselect_element(self, element):
        self.selected_element_identifiers.remove(element.identifier)
        self.update_diagrams(EditActionType.SELECTION)

    # ----------------------------------------------------------------------------------------------
    def get_selected_elements(self):
        return [self.get_element_by_identifier(identifier) for identifier in self.selected_element_identifiers]

    # ----------------------------------------------------------------------------------------------
    def deselect_all_elements(self):
        self.selected_element_identifiers = []
        self.update_diagrams(EditActionType.SELECTION)

    # ----------------------------------------------------------------------------------------------
    def delete_elements(self, elements):
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
        self.update_diagrams(EditActionType.VISUAL)

    # ----------------------------------------------------------------------------------------------
    def delete_interface(self, interface: Interface):
        self.interfaces.remove(interface)
        for message in self.messages:
            if message.interface == interface.name:
                self.delete_message(message)
        self.update_diagrams(EditActionType.NON_VISUAL)

    # ----------------------------------------------------------------------------------------------
    def delete_message(self, message: Message):
        action = EditActionType.NON_VISUAL
        self.messages.remove(message)
        for transition in self.transitions:
            if message.get_variable_name() in transition.messages:
                transition.messages.remove(message)
                action = EditActionType.VISUAL
        self.update_diagrams(action)

    # ----------------------------------------------------------------------------------------------
    def delete_state(self, state: State):
        self.states.remove(state)
        for transition in self.transitions:
            if transition.source_name == state.name or transition.target_name == state.name:
                self.delete_transition(transition)
        self.update_diagrams(EditActionType.VISUAL)

    # ----------------------------------------------------------------------------------------------
    def delete_choice_point(self, choice_point: ChoicePoint):
        self.choice_points.remove(choice_point)
        for transition in self.transitions:
            if transition.source_name == choice_point.name:
                self.delete_transition(transition)
        self.update_diagrams(EditActionType.VISUAL)
    # ----------------------------------------------------------------------------------------------
    def delete_transition(self, transition: Transition):
        self.transitions.remove(transition)
        self.update_diagrams(EditActionType.VISUAL)

    # ----------------------------------------------------------------------------------------------
    def add_history(self, plantuml_code: str):
        self.history.append(plantuml_code)
        self.current_history_index += 1
        self.history = self.history[:self.current_history_index+1]

    # ----------------------------------------------------------------------------------------------
    def undo(self):
        if self.current_history_index > 0:
            self.current_history_index -= 1
            self.set_plantuml_code(self.history[self.current_history_index])

    # ----------------------------------------------------------------------------------------------
    def redo(self):
        if self.current_history_index == len(self.history):
            return
        self.current_history_index += 1
        self.set_plantuml_code(self.history[self.current_history_index])

    # ----------------------------------------------------------------------------------------------
    def get_plantuml_code(self, code_type: CodeType) -> str:
        if code_type == CodeType.MASKED:
            plantuml_code = HEADER_MASKED_PLANTUML_CODE
        else:
            plantuml_code = HEADER_PLANTUML_CODE
        
        plantuml_code += DEFAULT_INTERFACES_PLANTUML_CODE + DEFAULT_MESSAGES_PLANTUML_CODE
        
        plantuml_code += "\n" + self.get_interfaces_plantuml_code()
        plantuml_code += "\n" + self.get_messages_plantuml_code()
        plantuml_code += "\n" + self.get_component_plantuml_code(code_type)
        plantuml_code += "\n" + self.get_states_plantuml_code(code_type)
        plantuml_code += "\n" + self.get_choice_points_plantuml_code(code_type)
        plantuml_code += "\n" + self.get_transitions_plantuml_code(code_type)

        plantuml_code += "\n" + FOOTER_PLANTUML_CODE
        return plantuml_code

    # ----------------------------------------------------------------------------------------------
    def get_interfaces_plantuml_code(self) -> str:
        plantuml_code = INTERFACES_PLANTUML_CODE
        for interface in self.interfaces:
            plantuml_code += f"{interface.get_plantuml_code()}\n"
        return plantuml_code

    # ----------------------------------------------------------------------------------------------
    def get_messages_plantuml_code(self) -> str:
        plantuml_code = MESSAGES_PLANTUML_CODE
        for message in self.messages:
            if message.name == "Timeout" or message.name == "No" or message.name == "Yes":
                continue
            plantuml_code += f"{message.get_plantuml_code()}\n"
        return plantuml_code

    # ----------------------------------------------------------------------------------------------
    def get_component_plantuml_code(self, code_type: CodeType) -> str:
        plantuml_code = f"{COMPONENT_PLANTUML_CODE}state component as \"{self.component_name}\" {{\nstate START <<start>> "
        if code_type == CodeType.SELECTED and 0 in self.selected_element_identifiers:
            plantuml_code += "#FF0000\n"
        else:
            plantuml_code += "#000000\n"
        return plantuml_code

    # ----------------------------------------------------------------------------------------------
    def get_states_plantuml_code(self, code_type: CodeType) -> str:
        plantuml_code = STATES_PLANTUML_CODE
        for state in self.states:
            if state.name == "START":
                continue
            state_code_type = CodeType.SELECTED if code_type == CodeType.SELECTED and state.identifier in self.selected_element_identifiers else code_type
            plantuml_code += f"{state.get_plantuml_code(state_code_type)}\n"
        return plantuml_code

    # ----------------------------------------------------------------------------------------------
    def get_choice_points_plantuml_code(self, code_type: CodeType) -> str:
        plantuml_code = CHOICE_POINTS_PLANTUML_CODE
        for choice_point in self.choice_points:
            choice_point_code_type = CodeType.SELECTED if code_type == CodeType.SELECTED and choice_point.identifier in self.selected_element_identifiers else code_type
            plantuml_code += f"{choice_point.get_plantuml_code(choice_point_code_type)}\n"
        return plantuml_code

    # ----------------------------------------------------------------------------------------------
    def get_transitions_plantuml_code(self, code_type: CodeType) -> str:
        plantuml_code = TRANSITIONS_PLANTUML_CODE
        for transition in self.transitions:
            transition_code_type = CodeType.SELECTED if code_type == CodeType.SELECTED and transition.identifier in self.selected_element_identifiers else code_type
            plantuml_code += f"{transition.get_plantuml_code(transition_code_type)}\n"
        return plantuml_code
