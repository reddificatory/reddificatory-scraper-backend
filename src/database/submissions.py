import os
import sys
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))
import random
import database.submissions
import database.connection
import logger

def store_submission(subreddit, submission_id, strong):    
    database.connection.cursor.execute(f"INSERT INTO submissions (submission_id, subreddit, strong) VALUES ('{submission_id}', '{subreddit}', '{strong}') ON CONFLICT DO NOTHING;")
    database.connection.database.commit()

def update_submission(submission_id, mode):
    database.connection.cursor.execute(f"UPDATE submissions SET {mode} = TRUE, updated_at = (current_timestamp) WHERE submission_id = '{submission_id}'")
    database.connection.database.commit()

def get_submissions_with_comments(subreddit):
    database.connection.cursor.execute(f"SELECT * FROM submissions WHERE used = FALSE AND scraped = TRUE AND subreddit = '{subreddit}';")
    return database.connection.cursor.fetchall()

def get_random_submission(subreddit):
    submissions = get_submissions_with_comments(subreddit)

    if len(submissions) == 0:
        logger.logger.error('No scraped submissions in database. Please run the scraper.')
        return False

    stop = len(submissions) - 1
    random_submission = submissions[random.randint(0, stop)]    
    return random_submission[0]

# TODO: figure out why it's printing two times
def get_submission_count(mode):
    mode_string = ''

    if mode == 'scraped':
        mode_string = ' WHERE scraped = true'

    if mode == 'used':
        mode_string = ' WHERE used = true'

    database.connection.cursor.execute(f"SELECT COUNT(*) FROM submissions {mode_string};")
    
    return database.connection.cursor.fetchone()[0]