import sys
sys.path.insert(0, 'D:\coding\python-reddit-tts\src\db')
sys.path.insert(0, 'D:\coding\python-reddit-tts\src')

from db.submissions import update_submission
from database import cursor, db
import random
import config

def store_comment(comment_id, submission_id):
    cursor.execute(f"INSERT INTO comments (comment_id, submission_id) VALUES ('{comment_id}', '{submission_id}') ON CONFLICT DO NOTHING;")    
    db.commit()

def update_comment(comment_id):
    cursor.execute(f"UPDATE comments SET used = TRUE, updated_at = (current_timestamp) WHERE comment_id = '{comment_id}';")
    db.commit()

def get_unused_comments_from_submission(submission_id):
    # cursor.execute(f"SELECT * FROM comments WHERE used = FALSE AND submission_id = {submission.id}")
    #TODO: corrrect this query
    cursor.execute(f"SELECT comments.comment_id FROM comments INNER JOIN submissions ON submissions.submission_id = comments.submission_id WHERE comments.submission_id IN (SELECT submission_id FROM comments GROUP BY submission_id HAVING COUNT(*) != 0) AND comments.submission_id = '{submission_id}';")
    comments = cursor.fetchall()
    comment_ids = []

    for comment in comments:
        comment_ids.append(comment[0])

    return comment_ids

def get_random_comment(submission_id):
    submission = config.REDDIT_CLIENT.submission(submission_id)
    comments = get_unused_comments_from_submission(submission_id)
    stop = len(comments) - 1

    print(submission_id)

    random_comment = comments[random.randint(0, stop)]
    return random_comment

def get_random_comments(submission_id, count):
    random_comments = set()
    for i in range(count):
        random_comments.add(get_random_comment(submission_id))
    
    update_submission(submission_id, 'used')
    
    return random_comments

#print(get_unused_comments_from_submission('11ark0w'))