import os
import sys
sys.path.insert(0, os.getcwd() + '/src')

import random
import db.submissions
import db.database

def store_submission(subreddit, submission_id):    
    db.database.cursor.execute(f"INSERT INTO submissions (submission_id, subreddit) VALUES ('{submission_id}', '{subreddit}') ON CONFLICT DO NOTHING;")    
    db.database.db.commit()

def update_submission(submission_id, mode):
    db.database.cursor.execute(f"UPDATE submissions SET {mode} = TRUE, updated_at = (current_timestamp) WHERE submission_id = '{submission_id}'")
    db.database.db.commit()

#TODO: finish this query and function
def get_submissions(mode):
    db.database.cursor.execute(f"SELECT * FROM submissions WHERE {mode} = FALSE;")
    return db.database.cursor.fetchall()

def get_submissions_with_comments():
    db.database.cursor.execute(f"SELECT * FROM submissions WHERE used = FALSE AND scraped = TRUE;")
    return db.database.cursor.fetchall()

def get_random_submission(mode):
    submissions = get_submissions(mode)

    if len(submissions) == 0:
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