from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

def decide_if_strong(polarity_score):
    if polarity_score['compound'] > 0.5 or polarity_score['compound'] < -0.5:
        return True
    
    return False

def is_strong(text):
    sentiment_instensity_analyzer = SIA()

    polarity_score = sentiment_instensity_analyzer.polarity_scores(text)
    return decide_if_strong(polarity_score)