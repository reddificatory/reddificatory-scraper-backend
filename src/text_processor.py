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
    line = ''
    words = text.split(' ')

    for word in words:
        if font.getlength(line) + font.getlength(word) <= max_width:
            line += f' {word}'
            # print('sorhoz:', word)
        else:
            processed_text += f'\n{line.strip()}'
            line = word
            # print('tores:', word)

    if line:
        processed_text += f'\n{line.strip()}'

    return processed_text

# def get_text_height(text, font):
#     height = 0
#     lines = text.strip().split('\n')

#     for line in lines:
#         height += font.getbbox(line)[3]

#     return height