import config
import praw
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

reddit = praw.Reddit(client_id = config.CLIENT_ID, client_secret = config.CLIENT_SECRET, user_agent = config.CLIENT_AGENT)
subreddit = reddit.subreddit('askreddit')

submissions = set()
for submission in subreddit.hot(limit = 10):
    submissions.add(submission)

df = pd.DataFrame(submissions)

df.to_csv('data/raw/titles.csv', header = False, index = False, encoding = 'utf-8')

sia = SIA()
scores = []

for x in submissions:
    pol_score = sia.polarity_scores(x.title)
    pol_score['submission'] = x
    scores.append(pol_score)

df = pd.DataFrame.from_records(scores)

for x in scores:
    df['strong'] = False
    df.loc[df['compound'] > 0.5, 'strong'] = True 
    df.loc[df['compound'] < -0.5, 'strong'] = True

# TODO: remove not strong sentiments from list
strong = df.to_dict()
for x in strong:
    print(strong[x])

df.to_csv('data/processed/scores.csv', header = False, index = False, encoding = 'utf-8')