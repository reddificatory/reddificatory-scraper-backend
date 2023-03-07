import sys
sys.path.insert(0, 'D:\coding\python-reddit-tts\src')

import pyttsx3
import os
import config
import db.submissions
import db.comments
import scraper.comment_scraper
import scraper.submission_scraper
import subtitle.subtitle_generator

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

def get_text(submission_id, comment_count):
    submission = config.REDDIT_CLIENT.submission(submission_id)
    subreddit = submission.subreddit.display_name
    title = submission.title
    comment_ids = db.comments.get_unused_comments(submission_id)
    text = f'r/{subreddit} {title}'

    try:
        i = 0
        while i < comment_count:
            comment = config.REDDIT_CLIENT.comment(id = comment_ids[i])
            text += ' ' + comment.body
            db.comments.update_comment(comment_ids[i])
            i += 1

    except:
        True

    db.submissions.update_submission(submission_id, 'used')

    return text.strip()

def check_save_path(submission_id):
    submission = config.REDDIT_CLIENT.submission(submission_id)
    subreddit = submission.subreddit.display_name
    save_path = f'videos/{subreddit}/{submission_id}'

    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    return save_path

def tts_say(submission_id, tts):
    text = get_text(submission_id, 3)
    tts.save_to_file(text, f'{check_save_path(submission_id)}/audio.mp3')

def tts_run():
    tts = config_tts()
    random_submission_id = tts_get_random_submission()
    tts_say(random_submission_id, tts)
    tts.runAndWait()