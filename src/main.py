import os
import config
import scraper
import file
import text_processor
import text_to_speech
import database.submissions
import database.comments

subreddit = 'askreddit'
scraper.scrape(subreddit)

submission_id = database.submissions.get_random_submission()

save_path = file.get_save_path(os.path.join('media', 'reddit'), submission_id)