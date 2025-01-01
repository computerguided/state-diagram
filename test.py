from plantuml_manager import PlantUMLManager, CodeType
from elements import Message

# Read the content of the file
with open("diagrams/empty.puml", "r") as file:
    plantuml_code = file.read()

plantuml_manager = PlantUMLManager()
print(f"1. {plantuml_manager.current_history_index}")
print(len(plantuml_manager.history))

plantuml_manager.load_diagram(plantuml_code)
print(f"2. {plantuml_manager.current_history_index}")
print(len(plantuml_manager.history))

plantuml_manager.add_interface("TestInterface")
print(f"3. {plantuml_manager.current_history_index}")
print(len(plantuml_manager.history))

plantuml_manager.undo()
print(f"4. {plantuml_manager.current_history_index}")
print(len(plantuml_manager.history))

plantuml_manager.add_message("TestInterface", "TestMessage")    
print(f"5. {plantuml_manager.current_history_index}")
print(len(plantuml_manager.history))

plantuml_manager.add_state("TestState")
print(f"6. {plantuml_manager.current_history_index}")
print(len(plantuml_manager.history))

plantuml_manager.add_transition("TestState", "TestState")
print(f"7. {plantuml_manager.current_history_index}")
print(len(plantuml_manager.history))
plantuml_manager.state_diagram.rendered_image.show()
