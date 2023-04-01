import os
import sys
sys.path.insert(0, os.getcwd() + '/src')

import database.submissions
import database.connection
import random
import config

def store_comment(comment_id, submission_id, comment_length, strong):
    database.connection.cursor.execute(f"INSERT INTO comments (comment_id, submission_id, length, strong) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;", (comment_id, submission_id, comment_length, strong))
    database.connection.database.commit()

def update_comment(comment_id):
    database.connection.cursor.execute(f"UPDATE comments SET used = TRUE, updated_at = (current_timestamp) WHERE comment_id = '{comment_id}';")
    database.connection.database.commit()

def get_unused_comments(submission_id, comment_count):
    database.connection.cursor.execute(f"SELECT comments.comment_id FROM comments INNER JOIN submissions ON submissions.submission_id = comments.submission_id WHERE comments.submission_id IN (SELECT submission_id FROM comments GROUP BY submission_id HAVING COUNT(*) != 0) AND comments.submission_id = '{submission_id}';")
    comments = database.connection.cursor.fetchall()
    comment_ids = []

    try:
        for i, comment in enumerate(comments):
            if i == comment_count:
                break

            comment_ids.append(comment[0])
    except:
        True

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
    
    database.submissions.update_submission(submission_id, 'used')

    return random_comment_ids