from database import cursor, db

def check_submission(id):
    cursor.execute(f"SELECT * FROM submissions WHERE submission_id = '{id}';")
    submission = cursor.fetchone()

    # [2] is used status
    if not submission[2]:
        return False
    
    return True

def store_submissions(submissions):
    for submission in submissions:
        print(submission.id)
        cursor.execute(f"INSERT INTO submissions (submission_id) VALUES ('{submission.id}') ON CONFLICT DO NOTHING;")
    
    db.commit()

def update_submission(submission_id):
    cursor.execute(f"UPDATE submissions SET used = TRUE, updated_at = (current_timestamp) WHERE submission_id = '{submission_id}'")
    db.commit()