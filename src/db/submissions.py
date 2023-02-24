import random
from database import cursor, db

def store_submission(submission_id):    
    cursor.execute(f"INSERT INTO submissions (submission_id) VALUES ('{submission_id}') ON CONFLICT DO NOTHING;")    
    db.commit()

def update_submission(submission_id, mode):
    cursor.execute(f"UPDATE submissions SET {mode} = TRUE, updated_at = (current_timestamp) WHERE submission_id = '{submission_id}'")
    db.commit()

#TODO: finish this query and function
def get_submissions(mode):
    cursor.execute(f"SELECT * FROM submissions WHERE {mode} = FALSE;")
    return cursor.fetchall()

def get_random_submission(mode):
    submissions = get_submissions(mode)    
    stop = len(submissions) - 1
    random_submission = submissions[random.randint(0, stop)]    
    return random_submission[0]

def has_comments(submission_id):
    cursor.execute(f"SELECT COUNT(*) FROM comments WHERE submission_id = '{submission_id}' HAVING COUNT(*) != 0;")
    
    try:
        result = cursor.fetchone()[0]
        return True
    except:
        return False