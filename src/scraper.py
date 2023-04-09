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

def get_submissions(subreddit, strong):
    client = config.REDDIT_CLIENT
    subreddit = client.subreddit(subreddit)
    submissions = set()
    
    logger.logger.debug(f'Getting submissions from {subreddit}...')
    for submission in subreddit.hot(limit = 25):
        if strong:
            if text_processor.is_strong(submission.title):
                submissions.add(submission)
                database.submissions.store_submission(subreddit, submission.id, text_processor.is_strong(submission.title))
        else:
            submissions.add(submission)
            database.submissions.store_submission(subreddit, submission.id, text_processor.is_strong(submission.title))

    return submissions

def get_comments(submission_id, strong):
    submission = config.REDDIT_CLIENT.submission(submission_id)
    comments = set()

    logger.logger.debug(f'Getting comments from {submission.id}...')
    submission.comments.replace_more(limit=0)
    for comment in submission.comments:
        author = comment.author
        # TODO: AttributeError: 'NoneType' object has no attribute 'is_mod'
        try:
            if strong and not author.is_mod:
                if text_processor.is_strong(comment.body):
                    comments.add(comment)
                    database.comments.store_comment(comment.id, submission.id, len(comment.body), text_processor.is_strong(comment.body))
            elif not author.is_mod:
                comments.add(comment)
                database.comments.store_comment(comment.id, submission.id, len(comment.body), text_processor.is_strong(comment.body))
        except:
            # TODO: figure out this problem
            pass

        database.submissions.update_submission(submission.id, 'scraped')

    return comments

def scrape(subreddit, strong):
    submissions = get_submissions(subreddit, strong)

    for submission in submissions:
        get_comments(submission.id, strong)

    logger.logger.debug("Scraping done.")

argument_parser = argparse.ArgumentParser()
subreddit_submission_group = argument_parser.add_mutually_exclusive_group(required=True)
subreddit_submission_group.add_argument('-s', '--subreddit', dest='subreddit', help='Subreddit to scrape')
subreddit_submission_group.add_argument('-u', '--submission', dest='submission', help='Submission to scrape')
argument_parser.add_argument('-S', '--strong', dest='strong', action='store_true', help='Scrape stuff with strong sentiments only')
arguments = argument_parser.parse_args()

def main():
    if arguments.submission and arguments.strong:
        argument_parser.error('The -S/--strong is not valid with the -u/--submission option')
    
    if arguments.submission:
        submission = config.REDDIT_CLIENT.submission(arguments.submission)
        database.submissions.store_submission(submission.subreddit, submission.id, text_processor.is_strong(submission.title))
        print(arguments)
        comments = get_comments(arguments.submission, arguments.strong)

    if arguments.subreddit:
        scrape(arguments.subreddit, arguments.strong)

    plyer.notification.notify(title='Reddit scraping', message=f'Finished scraping', app_name='Reddificatory Reddit Scarper')
    
if __name__ == '__main__':
    main()