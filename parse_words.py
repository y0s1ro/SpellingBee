import requests
from bs4 import BeautifulSoup
import json

def parse(link):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        page = requests.get(link, headers=headers).text
        soup = BeautifulSoup(page, 'lxml')
        words_block = soup.find_all('div', class_ = 'flex-list-item')
        words = []
        for word_block in words_block:
            word = word_block.get_text(strip=True) 
            words.append(word[:-1])

        central_letter, letters = find_letters(words)
        date = soup.find('div', id = 'date-and-pic').find('h2').get_text(strip=True)
        date = date.split('day, ')[1]
        create_json(date, central_letter, letters, words)
        return 0
    except:
        return "Error"
    

def find_letters(words):
    letters = {}
    for word in words:
        unique_letters = set(word)
        for letter in unique_letters:
            if letter in letters:
                letters[letter] += 1
            else:
                letters[letter] = 1
    central_letter = max(letters, key=letters.get)
    letters = letters.keys()
    letters = list(letters-{central_letter})
    return central_letter, letters

def create_json(date, central_letter, letters, words):
    data = {date: {
            'central letter': central_letter,
            'letters': letters,
            'words': words}
            }
    try:
        with open('words.json', 'r') as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = {}

    if date not in existing_data:
        existing_data.update(data)

        with open('words.json', 'w') as f:
            json.dump(existing_data, f, indent=4)


parse(f'https://nytbee.com/Bee_20241231.html')
