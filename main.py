import tkinter as tk
import math
import numpy as np
import json
import datetime
from parse_words import parse

# Size of the canvas
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 800

# Path to the file with words
PATH = 'words.json'

class Menu:
    def __init__(self, root):
        # Initialize the start menu canvas
        start_menu = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
        start_menu.pack()
        self.canvas = start_menu
        self.root = root
        self._create_menu()
    
    def _create_menu(self):
        # Create the menu frame
        menu_frame = tk.Frame(self.canvas, bg="white")
        menu_frame.place(x=CANVAS_WIDTH/2, y=40, anchor=tk.N)
        start_text = tk.Label(self.canvas, text="Choose level to play", font=("Arial", 20), bg="white", fg="black")
        start_text.place(x=CANVAS_WIDTH/2, y=10, anchor=tk.N)
        button_style = {
            "bg": "lightblue",       
            "fg": "black",        
            "font": ("Arial", 18),
            "bd": 0,              
            "highlightthickness": 0,  
            "relief": "flat", 
            "highlightbackground":"white"   
        }
        # Create buttons for each level
        with open(PATH, 'r') as f:
            data = json.load(f)
            for level in range(1, 32):
                if data[f'December {level}, 2024']['words_guessed'] != len(data[f'December {level}, 2024']['words'].keys()):
                    check_button = tk.Button(menu_frame, text=f"{level}\n{data[f'December {level}, 2024']['words_guessed']} words",
                                              command=lambda lvl=level: self._start_game(f'December {lvl}, 2024'), **button_style)
                    check_button.grid(row=(level-1)//6, column=(level-1)%6, padx=10, pady=10)
                else:
                    check_button = tk.Button(menu_frame, text=f"{level}\nCompleted", state='disabled', **button_style)
                    check_button.grid(row=(level-1)//6, column=(level-1)%6, padx=10, pady=10)
        # Add last played level button
        last_level_button = tk.Button(menu_frame, text=f"Last played\nlevel",
                                      command=lambda lvl=level: self._start_game('Last level'), **button_style)
        last_level_button.grid(row=5, column=1, padx=10, pady=10)
        # Add input field to load level by date
        input_frame = tk.Frame(self.canvas, bg="white")
        input_frame.place(x=CANVAS_WIDTH/2, y=CANVAS_HEIGHT-100, anchor=tk.S)

        input_label = tk.Label(input_frame, text="Enter date to load level from that day", font=("Arial", 15), bg="white", fg="black")
        input_label.pack(side=tk.LEFT, padx=10)

        self.input_var = tk.StringVar()
        input_entry = tk.Entry(input_frame, textvariable=self.input_var, font=("Arial", 15), bg="white", fg="black")
        input_entry.insert(0, "20250115")
        input_entry.pack(side=tk.LEFT, padx=10)

        input_button = tk.Button(input_frame, text="Load", command=self._load_level, **button_style)
        input_button.pack(side=tk.LEFT, padx=10)
    
    def _load_level(self):
        # Load the level based on the input date
        level = self.input_var.get()
        parse(f'https://nytbee.com/Bee_{level}.html')
        year = level[:4]
        month = level[4:6]
        day = level[6:]
        level = f"{datetime.date(1900, int(month), 1).strftime('%B')} {int(day)}, {year}"
        self._start_game(level)

    def _start_game(self, level):
        # Start the game for the selected level
        self.canvas.destroy()
        if level == 'Last level':
            with open(PATH, 'r') as f:
                data = json.load(f)
                level = data['Last level']
        words, letters, central_letter = read_words(PATH, level)
        game = tk.Canvas(self.root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
        game.pack()
        GUI(game, letters, central_letter, words, date=level)
        
class SideBar:
    def __init__(self, canvas, date):
        # Initialize the sidebar with found words
        self.found_words = []
        with open(PATH, 'r') as f:
            data = json.load(f)
            for word in data[date]['words']:
                if data[date]['words'][word]:
                    self.found_words.append(word)
        self.canvas = canvas
        self.sidebar_canvas = self._create_sidebar()
    
    def _create_sidebar(self):
        # Create the sidebar canvas
        width = CANVAS_HEIGHT/2-50
        height = CANVAS_HEIGHT-50
        rounded_label = tk.Canvas(self.canvas, width=width, height=height, bg="white", highlightthickness=0)
        rounded_label.place(x=CANVAS_WIDTH-25, y=CANVAS_HEIGHT/2, anchor=tk.E)
        
        # Draw rounded rectangle for the sidebar
        radius = 15
        rounded_label.create_arc((0, 0, radius, radius), start=90, extent=90, fill="lightgrey", outline="lightgrey")
        rounded_label.create_arc((width-radius, 0, width, radius), start=0, extent=90, fill="lightgrey", outline="lightgrey")
        rounded_label.create_arc((0, height-radius, radius, height), start=180, extent=90, fill="lightgrey", outline="lightgrey")
        rounded_label.create_arc((width-radius, height-radius, width, height), start=270, extent=90, fill="lightgrey", 
                                 outline="lightgrey")
        rounded_label.create_rectangle((radius/2, 0, width-radius/2, height), fill="lightgrey", outline="lightgrey")
        rounded_label.create_rectangle((0, radius/2, width, height-radius/2), fill="lightgrey", outline="lightgrey")
        
        # Display the number of found words
        rounded_label.create_text(width/2, 20, text=f"You found {len(self.found_words)} word", font=("Arial", 15), 
                                  fill="black", anchor=tk.CENTER, tags="word")

        # Display the found words
        for i, word in enumerate(self.found_words):
            rounded_label.create_text(width/2, 50 + 30*i, text=word, font=("Arial", 15), fill="black", 
                                      anchor=tk.CENTER, tags="word")
        
        return rounded_label

    def update_sidebar(self, found_word):
        # Update the sidebar with a new found word
        width = CANVAS_HEIGHT/2-50
        self.found_words.append(found_word)
        self.sidebar_canvas.delete("word")
        self.sidebar_canvas.create_text(width/2, 20, text=f"You found {len(self.found_words)} word", font=("Arial", 15), 
                                        fill="black", anchor=tk.CENTER, tags="word")
        words_limit = 23
        if len(self.found_words) > words_limit:
            for i, word in enumerate(self.found_words):
                if i < words_limit:
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
        # Initialize the hexagon button
        self.canvas = canvas
        self.text = text
        self.typed_word_var = typed_word
        self.hex_group_tag = create_hexagon(canvas, x, y, size, text, fill_color)
        canvas.tag_bind(self.hex_group_tag, "<Button-1>", self._on_hex_click)

    def _on_hex_click(self, event):
        # Handle hexagon button click
        current_text = self.typed_word_var.get()
        if len(current_text) < 15:
            self.typed_word_var.set(current_text + self.text)

class GUI:
    def __init__(self, canvas, letters, central_letter, words, date):
        # Initialize the game GUI
        self.canvas = canvas
        self.buttons = []
        self.letters = letters
        self.central_letter = central_letter
        self.words = words
        self.date = date
        self.typed_word, self.input_line = self._create_input_line()
        self._create_level_date()
        self._create_buttons(letters, central_letter)
        self._create_control_buttons()
        self.sidebar = SideBar(canvas, date)

        self.canvas.bind_all("<Key>", self._on_key_press)

    def _create_level_date(self):
        # Display the level date
        level_date = tk.Label(self.canvas, text=self.date, font=("Arial", 20), bg="white", fg="black")
        level_date.place(x=CANVAS_WIDTH/2-200, y=100, anchor=tk.CENTER)

    def _create_buttons(self, letters, central_letter):
        # Create hexagon buttons for each letter
        hex_centers = self._calculate_hexagons_centers(50, 0)
        np.random.shuffle(letters)
        for center, letter in zip(hex_centers, letters):
            hex_group_tag = HexagonButton(self.canvas, center[0], center[1], 50, letter, self.typed_word)
            self.buttons.append(hex_group_tag)
        hex_group_tag = HexagonButton(self.canvas, CANVAS_WIDTH/2-200, CANVAS_HEIGHT/2, 50, central_letter, self.typed_word, 
                                      'lightyellow')
        self.buttons.append(hex_group_tag)

    def _calculate_hexagons_centers(self, hex_size, hex_spacing):
        # Calculate the center positions for hexagon buttons
        canvas_center = (CANVAS_WIDTH/2-200, CANVAS_HEIGHT/2)
        hex_centers = []
        for i in range(6):
            angle = math.radians(60 * i + 30)
            x = canvas_center[0] + 2*(hex_size + hex_spacing) * math.cos(angle)
            y = canvas_center[1] + 2*(hex_size + hex_spacing) * math.sin(angle)
            hex_centers.append((x, y))
        return hex_centers
    
    def _create_input_line(self):
        # Create the input line for typed words
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
        # Create control buttons (Check, Delete, Shuffle, Menu)
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

        menu_button = tk.Button(self.canvas, text="Menu", command=self._return_to_menu, **button_style)
        menu_button.place(x=25, y=25, anchor=tk.NW)

    def _check_word(self):
        # Check if the typed word is valid
        if self.typed_word.get().lower() in self.words:
            self.sidebar.update_sidebar(self.typed_word.get().lower())
            self.display_message("Nice!")
        elif self.typed_word.get() == "":
            self.display_message("Enter a word")
        elif not all(char in (str(self.letters)+self.central_letter) for char in self.typed_word.get()):
            self.display_message("Bad letters")
        elif len(self.typed_word.get().lower()) < 4:
            self.display_message("Word is too short")
        elif self.central_letter not in self.typed_word.get():
            self.display_message("Central letter is missing")
        else:
            self.display_message("Not in word list")

    def _delete(self):
        # Delete the last character from the typed word
        self.typed_word.set(self.typed_word.get()[:-1])

    def _shuffle_letters(self):
        # Shuffle the letters
        self._create_buttons(self.letters, self.central_letter)

    def _return_to_menu(self):
        # Return to the main menu
        self.canvas.destroy()
        with open(PATH, 'r') as f:
            data = json.load(f)
        data['Last level'] = self.date
        with open(PATH, 'w') as f:
            json.dump(data, f, indent=4)
        Menu(self.canvas.master)

    def display_message(self, message):
        # Display a message on the canvas
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
            self.update_json(self.typed_word.get().lower())
            self.words.remove(self.typed_word.get().lower())
            if len(self.words) == 0:
                self.display_message("You found all words!")
                self.typed_word.set("")
                
        self.typed_word.set("")
    
    def update_json(self, word):
        # Update the JSON file with the found word
        with open(PATH, 'r') as f:
            data = json.load(f)
        data[self.date]['words'][word] = True
        data[self.date]['words_guessed'] += 1
        with open(PATH, 'w') as f:
            json.dump(data, f, indent=4)

    def _on_key_press(self, event):
        # Handle key press events
        if event.char.isalpha():
            current_text = self.typed_word.get()
            if len(current_text) < 15:
                self.typed_word.set(current_text + event.char.upper())
        elif event.keysym == "BackSpace":
            self._delete()
        elif event.keysym == "Return":
            self._check_word()

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
    hex_id = canvas.create_polygon(points, fill=fill_color, outline=outline_color, width=2, tags=group_tag)
    text_id = canvas.create_text(x, y, text=text, font=("Arial", int(size / 2)), fill="black", tags=group_tag)
    
    return group_tag

def read_words(path, date):
    # Read words from the JSON file for the given date
    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        return 'File not found'
    
    if date not in data:
        return 'Date not found'
    words = []
    for word in data[date]['words']:
        if not data[date]['words'][word]:
            words.append(word)
    letters = data[date]['letters']
    central_letter = data[date]['central letter']
    return words, letters, central_letter

def main():
    # Main function to start the application
    root = tk.Tk()
    root.title("Spelling Bee")

    Menu(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()
