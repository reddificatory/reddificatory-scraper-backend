import sys
sys.path.insert(0, 'D:\coding\Python\python-reddit-tts\src')

import pyttsx3
import os
import config
import db.submissions
import db.comments
import scraper.comment_scraper
import scraper.submission_scraper

def config_engine(rate):
    tts = pyttsx3.init()
    tts.setProperty('rate', rate)
    tts.setProperty('volume', 1)

    print('TTS config done...')

    return tts

def get_random_submission(subreddit):
    random_submission_id = db.submissions.get_random_submission_with_comments()

    if not random_submission_id:
        random_submission_id = db.submissions.get_random_submission('used')

        if not random_submission_id:
            print('Scraping submissions...')
            print(scraper.submission_scraper.scrape_subreddit(subreddit))
            random_submission_id = db.submissions.get_random_submission('used')

        print('Scraping comments...')
        print(scraper.comment_scraper.scrape_comments(random_submission_id))

    return random_submission_id

def process_text(text, max_line_length):
    lines = []
    line = ""

    for word in text.split():
        if len(line) + len(word) + 1 <= max_line_length:
            line += f" {word}"
        else:
            lines.append(line.strip())            
            line = word

    if line:
        lines.append(line.strip())

    return lines

def get_lines(submission_id, comment_count, max_line_length):
    submission = config.REDDIT_CLIENT.submission(submission_id)
    subreddit = submission.subreddit.display_name
    title = submission.title
    comment_ids = db.comments.get_unused_comments(submission_id)
    text = f'r/{subreddit}: {title}'
    # text = ''

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

    return process_text(text.strip().upper(), max_line_length)

def get_save_path(submission_id):
    submission = config.REDDIT_CLIENT.submission(submission_id)
    subreddit = submission.subreddit.display_name
    save_path = f'videos/{subreddit}/{submission_id}'

    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    return save_path

def save(submission_id, tts, max_line_length):
    lines = get_lines(submission_id, 3, max_line_length)
    save_path = get_save_path(submission_id)
    print('Saving text-to-speech output...')

    max_index_length = len(str(len(lines)))

    for i, line in enumerate(lines):
        index = i + 1
        index_length = len(str(index))

        if index_length < max_index_length:
            zero_digits_count = max_index_length - index_length
            zero_digits = ''

            for zero_digit in range(zero_digits_count):
                zero_digits += '0'

            index = f'{zero_digits}{index}'

        tts.save_to_file(line, f'{save_path}/audio{index}.wav')

    tts.runAndWait()

    print(f'Saved text-to-speech output to {save_path}/audio*.wav')
    return lines

# submission_id = '11lcyer'
# max_line_length = 40
# lines = get_text(submission_id, 3, max_line_length)
# max_index_length = len(str(len(lines)))
# # tts = config_engine(155)
# save_path = get_save_path(submission_id)

# for i, line in enumerate(lines):
#     index = i + 1
#     index_length = len(str(index))

#     if index_length < max_index_length:
#         zero_digits_count = max_index_length - index_length
#         zero_digits = ''

#         for zero_digit in range(zero_digits_count):
#             zero_digits += '0'

#         index = f'{zero_digits}{index}'

#     # tts.save_to_file(line, f'{save_path}/audio{index}.wav')

# # tts.runAndWait()