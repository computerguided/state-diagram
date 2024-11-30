from plantuml import PlantUML
from PIL import Image, ImageTk
import io

# Constants
PLANTUML_ENDPOINT = "http://www.plantuml.com/plantuml/png/"
DEFAULT_PLANTUML_CODE = """
@startuml
' == Formatting ==
hide empty description
skinparam Arrow {
  FontSize 9
}
skinparam State {
  FontSize 12
}

' == Default messages ==
!$Timeout = "Timeout"
!$No = No
!$Yes = Yes

' == Interfaces ==

' == Messages ==

state component as "Component Name" {
state START <<start>> #000000

' == States ==

' == Choice-points ==

' == Transitions ==

}
@enduml
"""

# -----------------------------------------------------------------------------
# Diagram class
# -----------------------------------------------------------------------------
class Diagram:
    def __init__(self):
        self.plantuml_client = PlantUML(PLANTUML_ENDPOINT)
        self.plantuml_code = DEFAULT_PLANTUML_CODE
        self.rendered_image = self.plantuml_client.processes(self.plantuml_code)

    # -------------------------------------------------------------------------
    def get_rendered_image(self, code: str) -> ImageTk.PhotoImage | None:
        try:
            raw_image_data = self.plantuml_client.processes(code)
            image = Image.open(io.BytesIO(raw_image_data))
            return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error rendering image: {e}")
            return None
        
    # -------------------------------------------------------------------------
    def set_plantuml_code(self, code: str) -> bool:
        temp_rendered_image = self.get_rendered_image(code)
        if not temp_rendered_image:
            return False
        self.plantuml_code = code
        self.rendered_image = temp_rendered_image
        return True