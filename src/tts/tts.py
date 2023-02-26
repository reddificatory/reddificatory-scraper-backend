import sys
sys.path.insert(0, 'D:\coding\python-reddit-tts\src')

import pyttsx3
import config
import db.submissions
import db.comments
import scraper.comment_scraper
import scraper.submission_scraper

def config_tts():
    tts = pyttsx3.init()
    tts.setProperty('rate', 160)
    tts.setProperty('volume', 1)

    print('TTS config done...')

    return tts

def tts_get_random_submission():
    random_submission_id = db.submissions.get_random_submission_with_comments()

    if not random_submission_id:
        random_submission_id = db.submissions.get_random_submission('used')

        if not random_submission_id:
            print('Scraping submissions...')
            print(scraper.submission_scraper.scrape_subreddit('askreddit'))
            random_submission_id = db.submissions.get_random_submission('used')

        print('Scraping comments...')
        print(scraper.comment_scraper.scrape_comments(random_submission_id))

    return random_submission_id

def tts_submission_details(submission_id, tts):
    submission = config.REDDIT_CLIENT.submission(submission_id)
    title = submission.title
    subreddit = f"r/{submission.subreddit.display_name}"

    print(subreddit)
    tts.say(subreddit)
    print(title)
    tts.say(title)

def tts_comments(submission_id, tts):
    comment_ids = db.comments.get_random_comments(submission_id, 3)

    for comment_id in comment_ids:
        comment = config.REDDIT_CLIENT.comment(id = comment_id)

        print(comment.body)
        #TODO save to file audio/{subreddit}/{submission_id}/{comment_id}.mp3
        tts.say(comment.body)
        db.comments.update_comment(comment_id)

    db.submissions.update_submission(submission_id, 'used')

def tts_run():
    tts = config_tts()
    random_submission_id = tts_get_random_submission()

    tts_submission_details(random_submission_id, tts)
    tts_comments(random_submission_id, tts)

    tts.runAndWait()