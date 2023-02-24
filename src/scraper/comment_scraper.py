import sys
sys.path.insert(0, 'D:\coding\python-reddit-tts\src\db')
sys.path.insert(0, 'D:\coding\python-reddit-tts\src')

import config
from db.comments import store_comment
from db.submissions import get_random_submission, update_submission
from sentiment_analyzer import is_strong
# from praw.models import MoreComments

def scrape_comments(submission):
    submission = config.REDDIT_CLIENT.submission(submission)
    comments = set()

    submission.comments.replace_more(limit=50)
    for comment in submission.comments:
        if is_strong(comment.body):
            comments.add(comment)
            store_comment(comment.id, submission.id)
            update_submission(submission.id, 'scraped')

    return comments

print(scrape_comments(get_random_submission('scraped')))