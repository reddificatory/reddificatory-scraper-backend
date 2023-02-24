import sys
sys.path.insert(0, 'D:\coding\python-reddit-tts\src\scraper')
sys.path.insert(0, 'D:\coding\python-reddit-tts\src\db')
sys.path.insert(0, 'D:\coding\python-reddit-tts\src')

import pyttsx3
import config
from db.submissions import get_random_submission, has_comments
from db.comments import get_random_comments

#TODO: select an unused submission, get some random comments, tts, save
random_submission = get_random_submission('used')
print(has_comments(random_submission))
comments = get_random_comments(random_submission, 3)
