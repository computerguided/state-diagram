# Data structures
_This section describes the data structures used in the application._


## Application

The `Application` class is the main class of the application. It is responsible for the GUI and the logic of the application.

To hold the GUI elements, the class has the following attributes:

- `root`: a `tk.Tk` object representing the root window.
- `main_content`: a `ttk.Frame` object representing the main content area.
- `toolbar`: a `ttk.Frame` object representing the toolbar.
- `protocol_panel`: a `ttk.Frame` object representing the protocol panel.
- `diagram_canvas`: a `ttk.Frame` object representing the diagram canvas.
- `properties_panel`: a `ttk.Frame` object representing the properties panel.

- `plantuml_manager`: a `PlantUMLManager` object.

It has the following methods:

- `