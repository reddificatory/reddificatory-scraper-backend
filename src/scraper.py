import os
import sys
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))
import config
import text_processor
import database.submissions
import database.comments
import logger
import argparse
import plyer

def get_submissions(subreddit, strong, limit):
    subreddit = config.REDDIT_CLIENT.subreddit(subreddit)
    submissions = set()

    if not limit:
        limit = len(subreddit.hot())
    
    logger.logger.debug(f'Getting submissions from {subreddit}...')

    for submission in subreddit.hot(limit=limit):
        if strong:
            if text_processor.is_strong(submission.title):
                submissions.add(submission)
                database.submissions.store_submission(subreddit, submission.id, text_processor.is_strong(submission.title))
        else:
            submissions.add(submission)
            database.submissions.store_submission(subreddit, submission.id, text_processor.is_strong(submission.title))

    return submissions

def get_comments(submission_id, strong, limit):
    submission = config.REDDIT_CLIENT.submission(submission_id)
    submission.comments.replace_more(limit=0)
    unscraped_comments = submission.comments
    comments = set()

    if not limit or limit > len(unscraped_comments):
        limit = len(unscraped_comments)

    logger.logger.debug(f'Getting comments from {submission.id}...')

    i = 0
    while i < limit:
        comment = unscraped_comments[i]
        author = comment.author

        # TODO: AttributeError: 'NoneType' object has no attribute 'is_mod'
        # TODO: find another method of identifying bots because is_mod is broken
        if strong:
            if text_processor.is_strong(comment.body):
                comments.add(comment)
                database.comments.store_comment(comment.id, submission.id, len(comment.body), text_processor.is_strong(comment.body))
        else:
            comments.add(comment)
            database.comments.store_comment(comment.id, submission.id, len(comment.body), text_processor.is_strong(comment.body))

        i += 1

        database.submissions.update_submission(submission.id, 'scraped')

    return comments

def scrape_submission(submission_id, strong, limit):
    submission = config.REDDIT_CLIENT.submission(submission_id)
    database.submissions.store_submission(submission.subreddit, submission.id, text_processor.is_strong(submission.title))
    comments = get_comments(submission.id, strong, limit)

def scrape_subreddit(subreddit, strong, limit_submissions, limit_comments):
    submissions = get_submissions(subreddit, strong, limit_submissions)

    for submission in submissions:
        get_comments(submission.id, strong, limit_comments)

    logger.logger.debug("Scraping done.")

argument_parser = argparse.ArgumentParser()
subreddit_submission_group = argument_parser.add_mutually_exclusive_group(required=True)
subreddit_submission_group.add_argument('-s', '--subreddit', dest='subreddit', help='Subreddit to scrape')
subreddit_submission_group.add_argument('-u', '--submission', dest='submission', help='Submission to scrape')
argument_parser.add_argument('-S', '--strong', dest='strong', action='store_true', help='Scrape stuff with strong sentiments only')
argument_parser.add_argument('-l', '--limit-submissions', type=int, dest='limit_submissions', default=25, help='Limit submission count')
argument_parser.add_argument('-L', '--limit-comments', type=int, dest='limit_comments', default=25, help='Limit comment count')
arguments = argument_parser.parse_args()

def main():
    if arguments.limit_submissions and arguments.submission:
        argument_parser.error('-l/--limit is invalid with -u/--submission.')

    if arguments.submission:
        scrape_submission(arguments.submission, arguments.strong, arguments.limit_comments)

    if arguments.subreddit:
        scrape_subreddit(arguments.subreddit, arguments.strong, arguments.limit_submissions, arguments.limit_comments)

    plyer.notification.notify(title='Reddit scraping', message=f'Finished scraping', app_name='Reddificatory Reddit Scarper')
    
if __name__ == '__main__':
    main()