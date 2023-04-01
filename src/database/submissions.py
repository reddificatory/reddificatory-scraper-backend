import os
import sys
sys.path.insert(0, os.getcwd() + '/src')

import random
import database.submissions
import database.connection

def store_submission(subreddit, submission_id, strong):    
    database.connection.cursor.execute(f"INSERT INTO submissions (submission_id, subreddit, strong) VALUES ('{submission_id}', '{subreddit}', '{strong}') ON CONFLICT DO NOTHING;")
    database.connection.database.commit()

def update_submission(submission_id, mode):
    database.connection.cursor.execute(f"UPDATE submissions SET {mode} = TRUE, updated_at = (current_timestamp) WHERE submission_id = '{submission_id}'")
    database.connection.database.commit()

#TODO: finish this query and function
def get_submissions(mode):
    database.connection.cursor.execute(f"SELECT * FROM submissions WHERE {mode} = FALSE;")
    return database.connection.cursor.fetchall()

def get_submissions_with_comments():
    database.connection.cursor.execute(f"SELECT * FROM submissions WHERE used = FALSE AND scraped = TRUE;")
    return database.connection.cursor.fetchall()

def get_random_submission():
    submissions = get_submissions_with_comments()

    if len(submissions) == 0:
        print('No scraped submissions in database. Please run the scraper.')
        return False

    stop = len(submissions) - 1
    random_submission = submissions[random.randint(0, stop)]    
    return random_submission[0]

def get_random_submission_with_comments():
    submissions = get_submissions_with_comments()

    if len(submissions) == 0:
        return False

    stop = len(submissions) - 1
    random_submission = submissions[random.randint(0, stop)]    
    return random_submission[0]