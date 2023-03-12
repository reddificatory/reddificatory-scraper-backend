import os
import sys
sys.path.insert(0, os.getcwd() + '/src')

import config

def get_save_path(submission_id):
    submission = config.REDDIT_CLIENT.submission(submission_id)
    subreddit = submission.subreddit.display_name
    save_path = f'media\\{subreddit}\\{submission_id}'

    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    return save_path

def get_file_name(object_list, index, file_name, file_extension):
    final_file_name = ''
    index += 1
    max_index_length = len(str(len(object_list)))
    index_length = len(str(index))

    if index_length < max_index_length:
        zero_digits_count = max_index_length - index_length
        zero_digits = ''

        for zero_digit in range(zero_digits_count):
            zero_digits += '0'

        index = f'{zero_digits}{index}'

    final_file_name = f'{file_name}{index}{file_extension}'

    return final_file_name, index