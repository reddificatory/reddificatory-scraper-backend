import os
import sys
sys.path.insert(0, os.getcwd() + '/src')
import config
import text_processor
import database.submissions

def scrape_subreddit(subreddit):
    client = config.REDDIT_CLIENT
    subreddit = client.subreddit(subreddit)
    submissions = set()
    
    for submission in subreddit.hot(limit = 50):
        if text_processor.is_strong(submission.title):
            submissions.add(submission)
            database.submissions.store_submission(subreddit, submission.id)

    return submissions

# print(scrape_subreddit('askreddit'))