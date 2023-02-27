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

def tts_say(submission_id, tts):
    submission = config.REDDIT_CLIENT.submission(submission_id)
    subreddit = submission.subreddit.display_name
    r_subreddit = f'r/{subreddit}'
    title = submission.title
    text = f'{r_subreddit} {title}'

    save_path = f'audio/{subreddit}'
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    print(r_subreddit)
    tts.save_to_file(r_subreddit, f'{save_path}/subreddit.mp3')

    save_path += f'/{submission_id}'
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    print(title)
    tts.save_to_file(title, f'{save_path}/title.mp3')

    comment_ids = db.comments.get_random_comments(submission_id, 3)

    for comment_id in comment_ids:
        comment = config.REDDIT_CLIENT.comment(id = comment_id)

        text += ' ' + comment.body
        print(comment.body)
        
        tts.save_to_file(comment.body, f'{save_path}/{comment_id}.mp3')
        db.comments.update_comment(comment_id)

    db.submissions.update_submission(submission_id, 'used')

def tts_run():
    tts = config_tts()
    random_submission_id = tts_get_random_submission()

    tts_say(random_submission_id, tts)

    tts.runAndWait()

tts_run()
