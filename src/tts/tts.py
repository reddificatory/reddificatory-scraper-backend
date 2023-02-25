import sys
sys.path.insert(0, 'D:\coding\python-reddit-tts\src')

import pyttsx3
import config
import db.submissions
import db.comments
import scraper.comment_scraper
import scraper.submission_scraper

random_submission_id = db.submissions.get_random_submission_with_comments()

if not random_submission_id:
    random_submission_id = db.submissions.get_random_submission('used')

    if not random_submission_id:
        print(scraper.submission_scraper.scrape_subreddit('askreddit'))
        random_submission_id = db.submissions.get_random_submission('used')

    print(scraper.comment_scraper.scrape_comments(random_submission_id))

tts = pyttsx3.init()
tts.setProperty('rate', 160)
tts.setProperty('volume', 1)

comment_ids = db.comments.get_random_comments(random_submission_id, 3)

for comment_id in comment_ids:
    comment = config.REDDIT_CLIENT.comment(id = comment_id)

    print(comment.body)
    tts.say(comment.body)
    tts.runAndWait()

    db.comments.update_comment(comment_id)

db.submissions.update_submission(random_submission_id, 'used')
