import sys
sys.path.insert(0, 'D:\coding\python-reddit-tts\src\scraper')
sys.path.insert(0, 'D:\coding\python-reddit-tts\src\db')

import pyttsx3
from db.comments import get_random_comment

#TODO: select an unused submission, get some random comments, tts, save

#print(get_random_comment())

# engine = pyttsx3.init()

# engine.setProperty('rate', 160)
# engine.setProperty('volume', 1)

# engine.save_to_file('i will speak this test text to be saved in a file', 'text.mp3')
# engine.runAndWait()