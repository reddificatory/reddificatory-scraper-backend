from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from PIL import Image, ImageFont
import re

def is_strong(text):
    sentiment_instensity_analyzer = SIA()

    polarity_score = sentiment_instensity_analyzer.polarity_scores(text)

    if polarity_score['compound'] > 0.5 or polarity_score['compound'] < -0.5:
        return True
    
    return False

# def get_font_height():
#     True

# def get_textbox_size():
#     True

def remove_duplicate_newlines(text):
    return re.sub('\n+', '\n', text).strip()

def wrap_text(text, max_width, font):
    processed_text = ''
    processing_line = ''
    lines = text.split('\n')

    for line in lines:
        words = line.split(' ')
        for word in words:
            if font.getlength(processing_line) + font.getlength(word) < max_width:
                processing_line += f' {word}'
            else:
                processed_text += f'\n{processing_line.strip()}'
                processing_line = word

        if processing_line:
            processed_text += f'\n{processing_line.strip()}'
            processing_line = ''
        
    return processed_text