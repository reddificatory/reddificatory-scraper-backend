import sys
sys.path.insert(0, 'D:\coding\python-reddit-tts\src')

import db.submissions
import db.database
import random
import config

def store_comment(comment_id, submission_id, comment_body):
    db.database.cursor.execute(f"INSERT INTO comments (comment_id, submission_id, body) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;", (comment_id, submission_id, comment_body))
    db.database.db.commit()

def update_comment(comment_id):
    db.database.cursor.execute(f"UPDATE comments SET used = TRUE, updated_at = (current_timestamp) WHERE comment_id = '{comment_id}';")
    db.database.db.commit()

def get_unused_comments(submission_id):
    db.database.cursor.execute(f"SELECT comments.comment_id FROM comments INNER JOIN submissions ON submissions.submission_id = comments.submission_id WHERE comments.submission_id IN (SELECT submission_id FROM comments GROUP BY submission_id HAVING COUNT(*) != 0) AND comments.submission_id = '{submission_id}';")
    comments = db.database.cursor.fetchall()
    comment_ids = []

    for comment in comments:
        comment_ids.append(comment[0])

    return comment_ids

def get_random_comment(submission_id):
    submission = config.REDDIT_CLIENT.submission(submission_id)
    comment_ids = get_unused_comments(submission_id)
    stop = len(comment_ids) - 1
    random_comment_id = comment_ids[random.randint(0, stop)]
    return random_comment_id

def get_random_comments(submission_id, count):
    random_comment_ids = set()
    for i in range(count):
        random_comment_ids.add(get_random_comment(submission_id))
    
    db.submissions.update_submission(submission_id, 'used')

    return random_comment_ids