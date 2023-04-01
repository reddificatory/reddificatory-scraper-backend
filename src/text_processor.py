from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

def is_strong(text):
    sentiment_instensity_analyzer = SIA()

    polarity_score = sentiment_instensity_analyzer.polarity_scores(text)

    if polarity_score['compound'] > 0.5 or polarity_score['compound'] < -0.5:
        return True
    
    return False

def get_font_height():
    True

def get_textbox_size():
    True