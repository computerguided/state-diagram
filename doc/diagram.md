# Diagram

_The `Diagram` class is responsible for holding the data of a diagram._

## Dependencies

The `Diagram` class depends on the `PlantUML` class from the `plantuml` package.

```python
from plantuml import PlantUML
```

The `Diagram` class also depends on the `Image` class and the `ImageTk` class (since we are using Tkinter) from the `PIL` package.

```python
from PIL import Image, ImageTk
```

Finally, the `io` module is used to handle the raw image data.

```python
import io
```

## Constants

The `Diagram` class has the following constants:

- `PLANTUML_ENDPOINT`: a string containing the endpoint of the PlantUML server.
- `DEFAULT_PLANTUML_CODE`: a string containing the default PlantUML code.

### PlantUML endpoint

The `PLANTUML_ENDPOINT` constant is used to set the endpoint of the PlantUML server.

```python
PLANTUML_ENDPOINT = "http://www.plantuml.com/plantuml/png/"
```

### Default PlantUML code

The `DEFAULT_PLANTUML_CODE` constant is used to set the default PlantUML code when a new diagram is created.

```python
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
```

## Attributes

The class has the following attributes:

- `plantuml_client`: a `PlantUML` object.
- `plantuml_code`: a string containing the PlantUML code.
- `rendered_image`: an `ImageTk.PhotoImage` object containing the rendered image of the PlantUML code. The `ImageTk.PhotoImage` is a class from the PIL (Pillow) library, specifically designed to handle images in a format that can be used with the Tkinter GUI toolkit. It allows you to display images in Tkinter widgets, such as labels or canvases.

## Constructor

The constructor of the class takes no arguments.

```python
def __init__(self):
```

First, the `PlantUML` client is created using the `PLANTUML_ENDPOINT` constant.

```python
self.plantuml_client = PlantUML(url=PLANTUML_ENDPOINT)
```

Then, the PlantUML code is set to the `DEFAULT_PLANTUML_CODE` constant.

```python
self.plantuml_code = DEFAULT_PLANTUML_CODE
```

Finally, the rendered image is updated with the new PlantUML code by calling the `processes` method of the `PlantUML` client.

```python
self.rendered_image = self.plantuml_client.processes(self.plantuml_code)
```

Note that it is ensured that the default PlantUML code is valid by construction and that no errors will occur when calling the `processes` method.

## Methods

The `Diagram` class has the following methods:

- [`get_rendered_image(code: str)`](#get_rendered_image): returns the rendered image of the PlantUML code.
- [`set_plantuml_code(code: str)`](#set_plantuml_code): sets the PlantUML code. This will also update the rendered image.

### Getting the rendered image

To get the rendered image, the `get_rendered_image` method can be called. This method will also check if the given PlantUML code is valid and return `None` if it is not.

```python
def get_rendered_image(self, code: str) -> ImageTk.PhotoImage | None:
```

To get the rendered image, the `processes` method of the `PlantUML` client can be called with the given PlantUML code. However, when the PlantUML code is invalid, the `processes` method will raise the `PlantUMLHTTPError` error. Therefore, this exception must be caught.

```python
try:
    raw_image_data = self.plantuml_client.processes(code)
    image = Image.open(io.BytesIO(raw_image_data))
    return ImageTk.PhotoImage(image)
except PlantUMLHTTPError:
    return None
```

### Setting the PlantUML code

To set the PlantUML code, the `set_plantuml_code` method can be called. The method will also update the rendered image. It will return `False` if the PlantUML code is invalid and `True` otherwise.

```python
def set_plantuml_code(self, code: str) -> bool:
```

First it is checked if the given PlantUML code is valid by calling the `get_rendered_image` method. If it is not valid, the method will return `False` and nothing will be changed.

```python
temp_rendered_image = self.get_rendered_image(code)
if not temp_rendered_image:
    return False
```

When the PlantUML code is valid, the rendered image is updated, the PlantUML code is set to the given string and the method will return `True`.

```python
self.rendered_image = temp_rendered_image
self.plantuml_code = code
return True
```

