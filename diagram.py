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

' == Component ==
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
        self.rendered_image = self.render_image(self.plantuml_code)
    # -------------------------------------------------------------------------
    def render_image(self, code: str) -> Image.Image | None:
        try:
            raw_image_data = self.plantuml_client.processes(code)
            return Image.open(io.BytesIO(raw_image_data))
        except Exception as e:
            print(f"Error rendering image: {e}")
            return None
        
    # -------------------------------------------------------------------------
    def set_plantuml_code(self, code: str) -> bool:
        temp_rendered_image = self.render_image(code)
        if not temp_rendered_image:
            return False
        self.plantuml_code = code
        self.rendered_image = temp_rendered_image
        return True