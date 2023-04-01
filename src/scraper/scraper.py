import os
import sys
sys.path.insert(0, os.getcwd() + '/src')
import config
import text_processor
import database.submissions

def get_submissions(subreddit):
    client = config.REDDIT_CLIENT
    subreddit = client.subreddit(subreddit)
    submissions = set()
    
    for submission in subreddit.hot(limit = 50):
        if text_processor.is_strong(submission.title):
            submissions.add(submission)
            database.submissions.store_submission(subreddit, submission.id, text_processor.is_strong(submission.title))

    return submissions

def get_comments(submission_id):
    submission = config.REDDIT_CLIENT.submission(submission_id)
    comments = set()

    submission.comments.replace_more(limit=20)
    for comment in submission.comments:
        comments.add(comment)
        database.comments.store_comment(comment.id, submission.id, len(comment.body), text_processor.is_strong(comment.body))
        database.submissions.update_submission(submission.id, 'scraped')

    return comments