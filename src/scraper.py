import os
import sys
sys.path.insert(0, os.getcwd() + '/src')
import config
import text_processor
import database.submissions
import logger

def get_submissions(subreddit):
    client = config.REDDIT_CLIENT
    subreddit = client.subreddit(subreddit)
    submissions = set()
    
    logger.logger.debug(f'Getting submissions from {subreddit}...')
    for submission in subreddit.hot(limit = 25):
        if text_processor.is_strong(submission.title):
            submissions.add(submission)
            database.submissions.store_submission(subreddit, submission.id, text_processor.is_strong(submission.title))

    return submissions

def get_comments(submission_id):
    submission = config.REDDIT_CLIENT.submission(submission_id)
    comments = set()

    logger.logger.debug(f'Getting comments from {submission.id}...')
    submission.comments.replace_more(limit=0)
    for comment in submission.comments:
        comments.add(comment)
        database.comments.store_comment(comment.id, submission.id, len(comment.body), text_processor.is_strong(comment.body))
        database.submissions.update_submission(submission.id, 'scraped')

    return comments

def scrape(subreddit):
    submissions = get_submissions(subreddit)

    for submission in submissions:
        get_comments(submission.id)

    logger.logger.debug("Scraping done.")