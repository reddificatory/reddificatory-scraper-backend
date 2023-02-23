import config
import praw
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

reddit = praw.Reddit(client_id = config.CLIENT_ID, client_secret = config.CLIENT_SECRET, user_agent = config.CLIENT_AGENT)

def collect_submissions(subreddit):
    submissions = set()
    for submission in subreddit.hot(limit = 50):
        submissions.add(submission)

    return submissions

def decide_strong_submissions(scores):
    df = pd.DataFrame(scores)
    
    for score in scores:
        df['strong'] = False
        df.loc[df['compound'] > 0.5, 'strong'] = True 
        df.loc[df['compound'] < -0.5, 'strong'] = True

    return df    

def get_strong_submissions(df):
    df_dict = df.to_dict()
    strongs = []
    i = 0

    for x in df_dict['strong']:
        if df_dict['strong'][i]:
            strongs.append(df_dict['submission'][i])

        i = i + 1

    return strongs

def analize_submissions(submissions):
    sia = SIA()
    scores = []

    for submission in submissions:
        pol_score = sia.polarity_scores(submission.title)
        pol_score['submission'] = submission
        scores.append(pol_score)

    decided = decide_strong_submissions(scores)
    strongs = get_strong_submissions(decided)

    return strongs

def scrape_subreddit(subreddit):
    subreddit = reddit.subreddit(subreddit)
    submissions = collect_submissions(subreddit)

    return analize_submissions(submissions)

# def scrape_submission(submissions):
#     for x in submissions:
#         for y in x.comments:
#             print(y.body)

# scrape_submission(scrape_subreddit('askreddit'))

print(scrape_subreddit('askreddit'))