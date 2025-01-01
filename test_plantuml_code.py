from plantuml_manager import PlantUMLManager, CodeType
from elements import Message

# Read the content of the file
with open("diagrams/node.puml", "r") as file:
    plantuml_code = file.read()

plantuml_manager = PlantUMLManager()

plantuml_manager.load_diagram(plantuml_code)

plantuml_manager.state_diagram.rendered_image.show()






