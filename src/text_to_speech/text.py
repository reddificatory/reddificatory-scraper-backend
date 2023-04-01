import os
import sys
sys.path.insert(0, os.getcwd() + '/src')

import config
import database.submissions
import scraper.comment_scraper
import scraper.submission_scraper

def get_random_submission(subreddit):
    random_submission_id = database.submissions.get_random_submission_with_comments()

    if not random_submission_id:
        random_submission_id = database.submissions.get_random_submission('used')

        if not random_submission_id:
            print('Scraping submissions...')
            print(scraper.submission_scraper.scrape_subreddit(subreddit))
            random_submission_id = database.submissions.get_random_submission('used')

        print('Scraping comments...')
        print(scraper.comment_scraper.scrape_comments(random_submission_id))

    return random_submission_id

def get_comments(submission_id, comment_count):
    comment_ids = database.comments.get_unused_comments(submission_id, comment_count)
    comments = []

    try:
        for comment_id in comment_ids:
            comment = config.REDDIT_CLIENT.comment(id=comment_id)
            comments.append(comment)
            database.comments.update_comment(comment_id)
    except:
        True

    database.submissions.update_submission(submission_id, 'used')

    return comments