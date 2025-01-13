import tkinter as tk
import math
import numpy as np

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 800


class HexagonButton:
    def __init__(self, canvas, x, y, size, text, fill_color='lightblue'):
        self.canvas = canvas
        self.text = text
        self.hex_group_tag = create_hexagon(canvas, x, y, size, text, fill_color)
        canvas.tag_bind(self.hex_group_tag, "<Button-1>", self.on_hex_click)

    def on_hex_click(self, event):
        print(self.hex_group_tag)

class LetterButtons:
    def __init__(self, canvas):
        self.canvas = canvas
        self.buttons = []
        self.create_buttons()

    def create_buttons(self):
        hex_centers = self._calculate_hexagons_centers(50, 0)
        #Create hexagons for each letter
        np.random.shuffle(letters)
        for center, letter in zip(hex_centers, letters):
            hex_group_tag = HexagonButton(self.canvas, center[0], center[1], 50, letter)
            self.buttons.append(hex_group_tag)
        hex_group_tag = HexagonButton(self.canvas, CANVAS_WIDTH/2, CANVAS_HEIGHT/2, 50, central_letter, 'lightyellow')
        self.buttons.append(hex_group_tag)

    def _calculate_hexagons_centers(self, hex_size, hex_spacing):
        canvas_center = (CANVAS_WIDTH/2, CANVAS_HEIGHT/2)  # Center of the canvas
        hex_centers = []
        #Calculates the center of each hexagon
        for i in range(6):
            angle = math.radians(60 * i + 30)
            x = canvas_center[0] + 2*(hex_size + hex_spacing) * math.cos(angle)
            y = canvas_center[1] + 2*(hex_size + hex_spacing) * math.sin(angle)
            hex_centers.append((x, y))
        return hex_centers


def create_hexagon(canvas, x, y, size, text, fill_color="lightblue", outline_color="black"):
    # Calculate the vertices of the hexagon
    points = []
    for i in range(6):
        angle = math.radians(60 * i)
        px = x + size * math.cos(angle)
        py = y + size * math.sin(angle)
        points.extend([px, py])
    
    # Draw the hexagon
    group_tag = f"hex_{text}"

    # Draw the hexagon and add the tag
    hex_id = canvas.create_polygon(points, fill=fill_color, outline=outline_color, width=2, tags=group_tag)
    
    # Add text in the center of the hexagon and add the same tag
    text_id = canvas.create_text(x, y, text=text, font=("Arial", int(size / 2)), fill="black", tags=group_tag)
    
    return group_tag

def main():
    global words, letters, central_letter
    words = open("words.txt").read().splitlines()[1:]
    letters = open("words.txt").read().splitlines()[0].split()[1:]
    central_letter = open("words.txt").read()[0]

    root = tk.Tk()
    root.title("Spelling Bee")
    
    canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
    canvas.pack()
    
    buttons = LetterButtons(canvas)

    root.mainloop()

if __name__ == "__main__":
    main()
