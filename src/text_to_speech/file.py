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