import sys
sys.path.insert(0, 'D:\coding\python-reddit-tts\src')

import config
import scraper.sentiment_analyzer
import db.submissions

def scrape_subreddit(subreddit):
    client = config.REDDIT_CLIENT
    subreddit = client.subreddit(subreddit)
    submissions = set()
    
    for submission in subreddit.hot(limit = 50):
        if scraper.sentiment_analyzer.is_strong(submission.title):
            submissions.add(submission)
            db.submissions.store_submission(submission.id)

    return submissions

# print(scrape_subreddit('askreddit'))