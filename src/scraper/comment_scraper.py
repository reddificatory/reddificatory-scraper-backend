import sys

sys.path.insert(0, 'D:\coding\python-reddit-tts\src\db')
sys.path.insert(0, 'D:\coding\python-reddit-tts\src')

import config
from db.comments import store_comment
from db.submissions import get_random_submission, update_submission
from sentiment_analyzer import is_strong
# from praw.models import MoreComments

def scrape_comments(client, submission):
    submission = client.submission(submission[0])
    comments = set()

    submission.comments.replace_more(limit=None)
    for comment in submission.comments:
        if is_strong(comment.body):
            comments.add(comment)
            store_comment(comment, submission)
            update_submission(submission)

    return comments

print(scrape_comments(config.REDDIT_CLIENT, get_random_submission()))
