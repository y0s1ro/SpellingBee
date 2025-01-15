import tkinter as tk
import math
import numpy as np

#Size of the canvas
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 800

PATH = 'words.txt' #Path to the file with words

class SideBar:
    def __init__(self, canvas):
        self.found_words = []
        self.canvas = canvas
        self.sidebar_canvas = self._create_sidebar()
    
    def _create_sidebar(self):
        width = CANVAS_HEIGHT/2-50
        height = CANVAS_HEIGHT-50
        rounded_label = tk.Canvas(self.canvas, width=width, height=height, bg="white", highlightthickness=0)
        rounded_label.place(x=CANVAS_WIDTH-25, y=CANVAS_HEIGHT/2, anchor=tk.E)
        
        
        radius = 15
        rounded_label.create_arc((0, 0, radius, radius), start=90, extent=90, fill="lightgrey", outline="lightgrey")
        rounded_label.create_arc((width-radius, 0, width, radius), start=0, extent=90, fill="lightgrey", outline="lightgrey")
        rounded_label.create_arc((0, height-radius, radius, height), start=180, extent=90, fill="lightgrey", outline="lightgrey")
        rounded_label.create_arc((width-radius, height-radius, width, height), start=270, extent=90, fill="lightgrey", 
                                 outline="lightgrey")
        rounded_label.create_rectangle((radius/2, 0, width-radius/2, height), fill="lightgrey", outline="lightgrey")
        rounded_label.create_rectangle((0, radius/2, width, height-radius/2), fill="lightgrey", outline="lightgrey")
        
        rounded_label.create_text(width/2, 20, text=f"You found {len(self.found_words)} word", font=("Arial", 15), 
                                  fill="black", anchor=tk.CENTER, tags="word")

        for i, word in enumerate(self.found_words):
            rounded_label.create_text(width/2, 50 + 30*i, text=word, font=("Arial", 15), fill="black", 
                                      anchor=tk.CENTER, tags="word")

        return rounded_label
    def update_sidebar(self, found_word):
        width = CANVAS_HEIGHT/2-50
        self.found_words.append(found_word)
        self.sidebar_canvas.delete("word")
        self.sidebar_canvas.create_text(width/2, 20, text=f"You found {len(self.found_words)} word", font=("Arial", 15), 
                                        fill="black", anchor=tk.CENTER, tags="word")
        words_limit = 23
        if len(self.found_words) > words_limit:
            for i, word in enumerate(self.found_words):
                if i<words_limit:
                    self.sidebar_canvas.create_text(100, 50 + 30*i, text=word, font=("Arial", 15), fill="black", 
                                                    anchor=tk.W, tags="word")
                else:
                    self.sidebar_canvas.create_text(width-100, 50 + 30*(i-words_limit), text=word, font=("Arial", 15), 
                                                    fill="black", anchor=tk.E, tags="word")
        else:
            for i, word in enumerate(self.found_words):
                self.sidebar_canvas.create_text(width/2, 50 + 30*i, text=word, font=("Arial", 15), fill="black", 
                                                anchor=tk.CENTER, tags="word")
class HexagonButton:
    def __init__(self, canvas, x, y, size, text, typed_word, fill_color='lightblue'):
        self.canvas = canvas
        self.text = text
        self.typed_word_var = typed_word
        self.hex_group_tag = create_hexagon(canvas, x, y, size, text, fill_color)
        canvas.tag_bind(self.hex_group_tag, "<Button-1>", self._on_hex_click)

    def _on_hex_click(self, event):
        current_text = self.typed_word_var.get()
        if len(current_text) < 15:
            self.typed_word_var.set(current_text + self.text)

class GUI:
    def __init__(self, canvas, letters, central_letter, words):
        self.canvas = canvas
        self.buttons = []
        self.letters = letters
        self.central_letter = central_letter
        self.words = words
        self.typed_word, self.input_line = self._create_input_line()
        self._create_buttons(letters, central_letter)
        self._create_control_buttons()
        self.sidebar = SideBar(canvas)

        self.canvas.bind_all("<Key>", self._on_key_press)
        
    def _create_buttons(self, letters, central_letter):
        hex_centers = self._calculate_hexagons_centers(50, 0)
        #Create hexagons for each letter
        np.random.shuffle(letters)
        for center, letter in zip(hex_centers, letters):
            hex_group_tag = HexagonButton(self.canvas, center[0], center[1], 50, letter, self.typed_word)
            self.buttons.append(hex_group_tag)
        hex_group_tag = HexagonButton(self.canvas, CANVAS_WIDTH/2-200, CANVAS_HEIGHT/2, 50, central_letter, self.typed_word, 
                                      'lightyellow')
        self.buttons.append(hex_group_tag)

    def _calculate_hexagons_centers(self, hex_size, hex_spacing):
        canvas_center = (CANVAS_WIDTH/2-200, CANVAS_HEIGHT/2)  #Center of the canvas
        hex_centers = []
        #Calculates the center of each hexagon
        for i in range(6):
            angle = math.radians(60 * i + 30)
            x = canvas_center[0] + 2*(hex_size + hex_spacing) * math.cos(angle)
            y = canvas_center[1] + 2*(hex_size + hex_spacing) * math.sin(angle)
            hex_centers.append((x, y))
        return hex_centers
    
    def _create_input_line(self):
        text_var = tk.StringVar()
        text_var.set("")
        typed_word = tk.Label(self.canvas, 
                            textvariable=text_var, 
                            anchor=tk.CENTER,       
                            justify=tk.CENTER,
                            bg = "white",
                            font=("Arial", 20),
                            fg="black",
                            underline=0
                            )
        typed_word.place(x=CANVAS_WIDTH/2-200, y=200, anchor=tk.CENTER)
        return text_var, typed_word
    
    def _create_control_buttons(self):
        button_style = {
            "bg": "white",       
            "fg": "black",        
            "font": ("Arial", 18),
            "bd": 0,              
            "highlightthickness": 0,  
            "relief": "flat", 
            "highlightbackground":"white"   
        }
        button_frame = tk.Frame(self.canvas, bg="white")
        button_frame.place(x=CANVAS_WIDTH/2-200, y=CANVAS_HEIGHT - 200, anchor=tk.CENTER)

        check_button = tk.Button(button_frame, text="Check", command=self._check_word, **button_style)
        check_button.pack(side=tk.LEFT, padx=10)

        clear_button = tk.Button(button_frame, text="Delete", command=self._delete, **button_style)
        clear_button.pack(side=tk.LEFT, padx=10)

        shuffle_button = tk.Button(button_frame, text="Shuffle", command=self._shuffle_letters, **button_style)
        shuffle_button.pack(side=tk.LEFT, padx=10)
        
    def _check_word(self):
        if self.typed_word.get().lower() in self.words:
            self.sidebar.update_sidebar(self.typed_word.get().lower())
            self.display_message("Nice!")
        elif self.typed_word.get() == "":
            self.display_message("Enter a word")
        #Check if the word contains only valid letters
        elif not all(char in (str(self.letters)+self.central_letter) for char in self.typed_word.get()):
            self.display_message("Bad letters")
        elif len(self.typed_word.get().lower()) < 4:
            self.display_message("Word is too short")
        elif self.central_letter not in self.typed_word.get():
            self.display_message("Central letter is missing")
        else:
            self.display_message("Not in word list")

    def _delete(self):
        self.typed_word.set(self.typed_word.get()[:-1])

    def _shuffle_letters(self):
        self._create_buttons(self.letters, self.central_letter)

    def display_message(self, message):
        width = len(message) * 7 + 10
        rounded_label = tk.Canvas(self.canvas, width=width, height=40, bg="white", highlightthickness=0)
        rounded_label.place(x=CANVAS_WIDTH/2-200, y=50, anchor=tk.CENTER)
        
        radius = 15
        rounded_label.create_arc((0, 0, radius, radius), start=90, extent=90, fill="lightgrey", outline="lightgrey")
        rounded_label.create_arc((width-radius, 0, width, radius), start=0, extent=90, fill="lightgrey", outline="lightgrey")
        rounded_label.create_arc((0, 40-radius, radius, 40), start=180, extent=90, fill="lightgrey", outline="lightgrey")
        rounded_label.create_arc((width-radius, 40-radius, width, 40), start=270, extent=90, fill="lightgrey", outline="lightgrey")
        rounded_label.create_rectangle((radius/2, 0, width-radius/2, 40), fill="lightgrey", outline="lightgrey")
        rounded_label.create_rectangle((0, radius/2, width, 40-radius/2), fill="lightgrey", outline="lightgrey")
        
        rounded_label.create_text(width/2, 20, text=message, font=("Arial", 15), fill="black", anchor=tk.CENTER)
        if len(self.words) != 0:
            self.canvas.after(800, rounded_label.destroy)
        if message == "Nice!":
            self.words.remove(self.typed_word.get().lower())
            if len(self.words) == 0:
                self.display_message("You found all words!")
                self.typed_word.set("")
                
        self.typed_word.set("")

    def _on_key_press(self, event):
        # Check if the pressed key is a valid letter
        if event.char.isalpha():  # Checks if the key is a letter
            current_text = self.typed_word.get()
            if len(current_text) < 15:
                self.typed_word.set(current_text + event.char.upper())
        elif event.keysym == "BackSpace":
            self._delete()
        elif event.keysym == "Return":
            self._check_word()
            

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
    words = list(map(str.lower, words))

    gui = GUI(canvas, letters, central_letter, words)

    root.mainloop()

if __name__ == "__main__":
    main()
