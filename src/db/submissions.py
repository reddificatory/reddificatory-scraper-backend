import random
from database import cursor, db

def store_submission(submission):    
    cursor.execute(f"INSERT INTO submissions (submission_id) VALUES ('{submission.id}') ON CONFLICT DO NOTHING;")    
    db.commit()

def update_submission(submission, mode):
    cursor.execute(f"UPDATE submissions SET {mode} = TRUE, updated_at = (current_timestamp) WHERE submission_id = '{submission.id}'")
    db.commit()

def get_submissions(mode):
    cursor.execute(f"SELECT * FROM submissions WHERE {mode} = FALSE;")
    return cursor.fetchall()

def get_random_submission(mode):
    submissions = get_submissions(mode)    
    stop = len(submissions) - 1
    random_submission = submissions[random.randint(0, stop)]
    return random_submission

