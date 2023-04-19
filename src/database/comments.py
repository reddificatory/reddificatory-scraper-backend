import os
import sys
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))
import database.submissions
import database.connection
import re

def store_comment(comment_id, submission_id, comment_length, strong):
    database.connection.cursor.execute(f"INSERT INTO comments (comment_id, submission_id, length, strong) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING;", (comment_id, submission_id, comment_length, strong))
    database.connection.database.commit()

def update_comment(comment_id):
    database.connection.cursor.execute(f"UPDATE comments SET used = TRUE, updated_at = (current_timestamp) WHERE comment_id = '{comment_id}';")
    database.connection.database.commit()

def get_comments(submission_id, max_length=False, comment_count=False, strong=False):
    max_length_string = ''
    limit_string = ''
    strong_string = ''
    if max_length:
        max_length_string = f'AND comments.length <= {max_length}'
    if comment_count:
        limit_string = f'LIMIT {comment_count}'
    if strong:
        strong_string = f'AND comments.strong = {strong}'

    command = re.sub(' +', ' ', f"SELECT comments.comment_id FROM comments INNER JOIN submissions ON submissions.submission_id = comments.submission_id WHERE comments.submission_id IN (SELECT submission_id FROM comments GROUP BY submission_id HAVING COUNT(*) != 0) AND comments.submission_id = '{submission_id}' {max_length_string} {strong_string} ORDER BY comments.created_at {limit_string};")
    database.connection.cursor.execute(command)
    comments = database.connection.cursor.fetchall()
    comment_ids = []

    try:
        i = 0
        while i < comment_count:
            comment_ids.append(comments[i][0])
            i += 1
    except:
        pass

    return comment_ids