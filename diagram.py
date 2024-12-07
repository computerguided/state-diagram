from plantuml import PlantUML
from PIL import Image
import io

# Constants
DEFAULT_PLANTUML_CODE = """
@startuml
@enduml
"""

# -----------------------------------------------------------------------------
# Diagram class
# -----------------------------------------------------------------------------
class Diagram:
    def __init__(self, plantuml_endpoint: str):
        self.plantuml_client = PlantUML(plantuml_endpoint)
        self.plantuml_code = DEFAULT_PLANTUML_CODE
        self.rendered_image = self.render_image(self.plantuml_code)
    # -------------------------------------------------------------------------
    def render_image(self, code: str) -> Image.Image | None:
        try:
            raw_image_data = self.plantuml_client.processes(code)
            return Image.open(io.BytesIO(raw_image_data))
        except Exception as e:
            print(f"ERROR: failed rendering image: {e}\nCode: {code}")
            return None
        
    # -------------------------------------------------------------------------
    def set_plantuml_code(self, code: str) -> bool:
        temp_rendered_image = self.render_image(code)
        if not temp_rendered_image:
            return False
        self.plantuml_code = code
        self.rendered_image = temp_rendered_image
        return True