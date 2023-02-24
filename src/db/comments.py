from database import cursor, db
import random

def store_comment(comment, submission):
    cursor.execute(f"INSERT INTO comments (comment_id, submission_id) VALUES ('{comment.id}', '{submission.id}') ON CONFLICT DO NOTHING;")    
    db.commit()

def update_comment(comment):
    cursor.execute(f"UPDATE comments SET used = TRUE, updated_at = (current_timestamp) WHERE comment_id = '{comment.id}'")
    db.commit()

def get_unused_comments_from_submission(submisson):
    cursor.execute(f"SELECT * FROM comments WHERE used = FALSE AND submission_id = '{submisson.id}';")
    return cursor.fetchall()

def get_random_comment(submission):
    comments = get_unused_comments_from_submission(submisson)    
    stop = len(comments) - 1
    random_comment = comments[random.randint(0, stop)]
    return random_comment

# TODO: finish this function
def get_random_comments(submission, count):
    comments = get_unused_comments_from_submission(submission)    
    stop = len(comments) - 1
    random_comment = comments[random.randint(0, stop)]
    return random_comment
