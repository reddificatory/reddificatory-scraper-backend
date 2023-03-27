import os
import sys
sys.path.insert(0, os.getcwd() + '/src')

import config
import db.comments
import db.submissions
import scraper.sentiment_analyzer

def scrape_comments(submission_id):
    submission = config.REDDIT_CLIENT.submission(submission_id)
    comments = set()

    submission.comments.replace_more(limit=20)
    for comment in submission.comments:
        # if scraper.sentiment_analyzer.is_strong(comment.body):
        comments.add(comment)
        db.comments.store_comment(comment.id, submission.id, len(comment.body))
        db.submissions.update_submission(submission.id, 'scraped')

    return comments

# random_submission = db.submissions.get_random_submission('used')

# if not random_submission:
#     print('No submissions to scrape')
# else:
#     print(scrape_comments(random_submission))