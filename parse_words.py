import requests
from bs4 import BeautifulSoup
import json

def parse(link):
    # Set up headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    # Get the page content
    page = requests.get(link, headers=headers).text
    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(page, 'lxml')
    # Find all word blocks
    words_block = soup.find_all('div', class_ = 'flex-list-item')
    words = []
    # Extract words from the word blocks
    for word_block in words_block:
        word = word_block.get_text(strip=True) 
        words.append(word[:-1])

    # Find the central letter and other letters
    central_letter, letters = find_letters(words)
    # Extract the date from the page
    date = soup.find('div', id = 'date-and-pic').find('h2').get_text(strip=True)
    date = date.split('day, ')[1]
    # Create a JSON file with the extracted data
    create_json(date, central_letter, letters, words)
    return 0
    

def find_letters(words):
    letters = {}
    # Count the occurrence of each letter in the words
    for word in words:
        unique_letters = set(word)
        for letter in unique_letters:
            if letter in letters:
                letters[letter] += 1
            else:
                letters[letter] = 1
    # Find the central letter (the most frequent one)
    central_letter = max(letters, key=letters.get)
    # Get the list of other letters
    letters = letters.keys()
    letters = list(letters - {central_letter})
    return central_letter.upper(), [key.upper() for key in letters]
    

def create_json(date, central_letter, letters, words):
    # Create a dictionary of words with a guessed status
    words_dict = {word: False for word in words}
    data = {date: {
            'words_guessed': 0,
            'central letter': central_letter,
            'letters': letters,
            'words': words_dict}
            }
    try:
        # Try to read existing data from the JSON file
        with open('words.json', 'r') as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        # If the file does not exist, create an empty dictionary
        existing_data = {}

    # Update the existing data with the new data
    if date not in existing_data:
        existing_data.update(data)
        # Write the updated data back to the JSON file
        with open('words.json', 'w') as f:
            json.dump(existing_data, f, indent=4)
