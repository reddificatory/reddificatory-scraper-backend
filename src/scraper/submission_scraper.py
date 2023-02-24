import sys
sys.path.insert(0, 'D:\coding\python-reddit-tts\src\db')
sys.path.insert(0, 'D:\coding\python-reddit-tts\src')

import config
from submissions import store_submission
import praw
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

REDDIT = praw.Reddit(client_id = config.CLIENT_ID, client_secret = config.CLIENT_SECRET, user_agent = config.CLIENT_AGENT)

def decide_if_strong(polarity_score):
    if polarity_score['compound'] > 0.5 or polarity_score['compound'] < -0.5:
        return True
    
    return False

def analyze_submission(submission):
    sentiment_instensity_analyzer = SIA()

    polarity_score = sentiment_instensity_analyzer.polarity_scores(submission.title)
    return decide_if_strong(polarity_score)

def scrape_subreddit(client, subreddit):
    subreddit = client.subreddit(subreddit)
    submissions = set()
    
    for submission in subreddit.hot(limit = 50):
        if analyze_submission(submission):
            submissions.add(submission)
            store_submission(submission)

    return submissions

print(scrape_subreddit(REDDIT, 'askreddit'))