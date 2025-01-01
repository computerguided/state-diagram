import tkinter as tk
from PIL import Image, ImageTk
from plantuml_manager import PlantUMLManager

class DiagramApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Diagram Viewer")

        # Create a canvas to display the diagram
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

        # Initialize PlantUMLManager
        self.plantuml_manager = PlantUMLManager()

        # Load and render the diagram
        self.load_and_display_diagram()

    def load_and_display_diagram(self):
        with open("diagrams/node.puml", "r") as file:
            plantuml_code = file.read()

        # Load the diagram
        self.plantuml_manager.load_diagram(plantuml_code)

        # Get the rendered image
        image = self.plantuml_manager.state_diagram.rendered_image

        # Convert the image to a format Tkinter can use
        self.tk_image = ImageTk.PhotoImage(image)

        # Display the image on the canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = DiagramApp(root)
    root.mainloop()
