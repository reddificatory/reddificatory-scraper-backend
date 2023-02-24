import sys
sys.path.insert(0, 'D:\coding\python-reddit-tts\src\db')
sys.path.insert(0, 'D:\coding\python-reddit-tts\src')

import config
from sentiment_analyzer import is_strong
from db.submissions import store_submission

def scrape_subreddit(subreddit):
    client = config.REDDIT_CLIENT
    subreddit = client.subreddit(subreddit)
    submissions = set()
    
    for submission in subreddit.hot(limit = 50):
        if is_strong(submission.title):
            submissions.add(submission)
            store_submission(submission.id)

    return submissions

# TODO: when done with code, remove print
print(scrape_subreddit('askreddit'))