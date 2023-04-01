import os
import sys
sys.path.insert(0, os.getcwd() + '/src')

import config

def get_save_path(root_path, submission_id):
    submission = config.REDDIT_CLIENT.submission(submission_id)
    subreddit = submission.subreddit.display_name
    save_path = os.path.join(root_path, subreddit, submission_id)

    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    return save_path

def get_index(list_length, index):
    index += 1
    max_index_length = len(str(list_length))
    index_length = len(str(index))

    if index_length < max_index_length:
        zero_digits_count = max_index_length - index_length
        zero_digits = ''

        for zero_digit in range(zero_digits_count):
            zero_digits += '0'

        index = f'{zero_digits}{index}'

    return index
