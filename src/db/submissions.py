from database import cursor, db
import random

def store_submission(submission):    
    cursor.execute(f"INSERT INTO submissions (submission_id) VALUES ('{submission.id}') ON CONFLICT DO NOTHING;")    
    db.commit()

def update_submission(submission):
    cursor.execute(f"UPDATE submissions SET used = TRUE, updated_at = (current_timestamp) WHERE submission_id = '{submission.id}'")
    db.commit()

def get_unused_submissions():
    cursor.execute(f"SELECT * FROM submissions WHERE used = FALSE;")
    return cursor.fetchall()

def get_random_submission():
    submissions = get_unused_submissions()    
    stop = len(submissions) - 1
    random_submission = submissions[random.randint(0, stop)]
    return random_submission

