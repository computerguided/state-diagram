# Diagram

_The `Diagram` class is responsible for holding the data of a diagram. It is generic as it doesn't assume the PlantUML type of the diagram._

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

The class has the following constants:

- `DEFAULT_PLANTUML_CODE`: a string containing the default PlantUML code.

```python
DEFAULT_PLANTUML_CODE = """
@startuml
@enduml
"""
```

## Attributes

The class has the following attributes:

- `plantuml_client`: a `PlantUML` object.
- `plantuml_code`: a string containing the PlantUML code.
- `rendered_image`: an `Image.Image` object containing the rendered image of the PlantUML code. The `Image.Image` is a class from the PIL (Pillow) library.

## Constructor

The constructor of the class takes no arguments.

```python
def __init__(self, plantuml_endpoint: str):
```

First, the `PlantUML` client is created using the `plantuml_endpoint` argument.

```python
self.plantuml_client = PlantUML(url=plantuml_endpoint)
```

Then, the PlantUML code is set to the `DEFAULT_PLANTUML_CODE` constant.

```python
self.plantuml_code = DEFAULT_PLANTUML_CODE
```

Finally, the rendered image is updated with the new PlantUML code by calling the `render_image` method.

```python
self.rendered_image = self.render_image(self.plantuml_code)
```

Note that the `render_image` method will also check if the given PlantUML code is valid and return `None` if it is not.

## Methods

The `Diagram` class has the following methods:

- [`rendered_image(code: str)`](#rendered_image): returns the rendered image of the PlantUML code.
- [`set_plantuml_code(code: str)`](#set_plantuml_code): sets the PlantUML code. This will also update the rendered image.

### Rendering the image

To get the rendered image, the `render_image` method can be called. This method will also check if the given PlantUML code is valid and return `None` if it is not.

```python
def render_image(self, code: str) -> Image.Image | None:
```

To get the rendered image, the `processes` method of the `PlantUML` client can be called with the given PlantUML code. When something goes wrong, the `processes` method will raise an exception which must be caught.

There are two types of exceptions that can be raised:

- Server is busy: the first argument of the exception will be the number `54`.
- Invalid PlantUML code: is assumed to be any other type of error.

When the PlantUML server is busy, the `render_image` method will retry until the PlantUML server is not busy anymore. to do this, `succeeded` is set to `False` and the method will keep retrying until the PlantUML server is not busy anymore.

```python
succeeded = False

while not succeeded:
    try:
        raw_image_data = self.plantuml_client.processes(code)
        succeeded = True
        image = Image.open(io.BytesIO(raw_image_data))
        return image
    except Exception as e:
        if e.args[0] == 54:
            print("PlantUML server is busy, retrying...")
        else:
            print(f"ERROR: failed rendering image: {e}\nCode: {code}")
            print(f"Unknown error {e.args[0]}, failing...")
            return None
```

### Setting the PlantUML code

To set the PlantUML code, the `set_plantuml_code` method can be called. The method will also update the rendered image. It will return `False` if the PlantUML code is invalid and `True` otherwise.

```python
def set_plantuml_code(self, code: str) -> bool:
```

First it is checked if the given PlantUML code is valid by calling the `render_image` method. If it is not valid, the method will return `False` and nothing will be changed.

```python
temp_rendered_image = self.render_image(code)
if not temp_rendered_image:
    return False
```

When the PlantUML code is valid, the rendered image is updated, the PlantUML code is set to the given string and the method will return `True`.

```python
self.rendered_image = temp_rendered_image
self.plantuml_code = code
return True
```

