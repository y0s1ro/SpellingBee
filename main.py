import tkinter as tk
import math
import numpy as np

#Size of the canvas
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 800

PATH = 'words.txt' #Path to the file with words

class HexagonButton:
    def __init__(self, canvas, x, y, size, text, typed_word,  fill_color='lightblue'):
        self.canvas = canvas
        self.text = text
        self.typed_word_var = typed_word
        self.hex_group_tag = create_hexagon(canvas, x, y, size, text, fill_color)
        canvas.tag_bind(self.hex_group_tag, "<Button-1>", self._on_hex_click)

    def _on_hex_click(self, event):
        # Update the StringVar to append the letter
        current_text = self.typed_word_var.get()
        self.typed_word_var.set(current_text + self.text)

class GUI:
    def __init__(self, canvas, letters, central_letter):
        self.canvas = canvas
        self.buttons = []
        self.typed_word, self.input_line = create_input_line(canvas)
        self.create_buttons(letters, central_letter)
        

    def create_buttons(self, letters, central_letter):
        hex_centers = self._calculate_hexagons_centers(50, 0)
        #Create hexagons for each letter
        np.random.shuffle(letters)
        for center, letter in zip(hex_centers, letters):
            hex_group_tag = HexagonButton(self.canvas, center[0], center[1], 50, letter, self.typed_word)
            self.buttons.append(hex_group_tag)
        hex_group_tag = HexagonButton(self.canvas, CANVAS_WIDTH/2, CANVAS_HEIGHT/2, 50, central_letter, self.typed_word, 'lightyellow')
        self.buttons.append(hex_group_tag)

    def _calculate_hexagons_centers(self, hex_size, hex_spacing):
        canvas_center = (CANVAS_WIDTH/2, CANVAS_HEIGHT/2)  #Center of the canvas
        hex_centers = []
        #Calculates the center of each hexagon
        for i in range(6):
            angle = math.radians(60 * i + 30)
            x = canvas_center[0] + 2*(hex_size + hex_spacing) * math.cos(angle)
            y = canvas_center[1] + 2*(hex_size + hex_spacing) * math.sin(angle)
            hex_centers.append((x, y))
        return hex_centers
    
def create_input_line(canvas):
    text_var = tk.StringVar()
    text_var.set("")
    typed_word = tk.Label(canvas, 
                        textvariable=text_var, 
                        anchor=tk.CENTER,       
                        justify=tk.CENTER,
                        bg = "white",
                        font=("Arial", 20),
                        fg="black",
                        underline=0
                        )
    typed_word.place(x=400, y=200, anchor=tk.CENTER)
    return text_var, typed_word


def create_hexagon(canvas, x, y, size, text, fill_color="lightblue", outline_color="black"):
    #Calculate the vertices of the hexagon
    points = []
    for i in range(6):
        angle = math.radians(60 * i)
        px = x + size * math.cos(angle)
        py = y + size * math.sin(angle)
        points.extend([px, py])
    
    #Draw the hexagon
    group_tag = f"hex_{text}"

    #Draw the hexagon and add the tag
    hex_id = canvas.create_polygon(points, fill=fill_color, outline=outline_color, width=2, tags=group_tag)
    
    #Add text in the center of the hexagon and add the same tag
    text_id = canvas.create_text(x, y, text=text, font=("Arial", int(size / 2)), fill="black", tags=group_tag)
    
    return group_tag


def read_words(path):
    words = open(path).read().splitlines()[1:]
    letters = open(path).read().splitlines()[0].split()[1:]
    central_letter = open(path).read()[0]
    return words, letters, central_letter

def main():
    root = tk.Tk()
    root.title("Spelling Bee")
    
    canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
    canvas.pack()

    #Read words from a file
    words, letters, central_letter = read_words(PATH)

    buttons = GUI(canvas, letters, central_letter)

    root.mainloop()

if __name__ == "__main__":
    main()
