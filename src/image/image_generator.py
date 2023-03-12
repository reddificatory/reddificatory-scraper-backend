import os
import sys
sys.path.insert(0, os.getcwd() + '/src')
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageColor
import urllib.request
import text_to_speech.file

def get_profile_pic(author, save_path, index):
    file_name = f'icon{index}.png'
    path = os.path.join(save_path, file_name)

    if not os.path.exists(path):
        urllib.request.urlretrieve(author.icon_img, path)
        icon_image = Image.open(path)
        icon_image.thumbnail((30, 30))
        icon_image.save(path)

    return Image.open(path)

def get_mask(image, save_path):
    path = os.path.join(save_path, 'mask.png')

    # if not os.path.exists:
    mask_image = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask_image)
    draw.ellipse((0, 0, 29, 29 ), 255)
    mask_image = mask_image.filter(ImageFilter.GaussianBlur(0.6))
    mask_image.save(path)

    return Image.open(path)

def process_text(text, width, font, margin, icon):
    processed_text = ''
    line = ''
    max_width = width - (3 * margin) - icon.width
    text = text.replace('\n\n', '\n').strip()
    words = text.split(' ')

    for word in words:
        if font.getlength(line) + font.getlength(word) <= max_width:
            line += f' {word}'
        else:
            processed_text += f'\n{line.strip()}'
            line = word

    if line:
        processed_text += f'\n{line.strip()}'

    return processed_text

def get_text_height(text, font):
    height = 0
    lines = text.strip().split('\n')

    for line in lines:
        height += font.getbbox(line)[3]

    return height

def generate_comment_picture(comment, save_path, file_name, index):
    author = comment.author
    icon = get_profile_pic(author, save_path, index)
    username = author.name
    body = comment.body
    score = comment.score
    
    header_font = ImageFont.truetype('C:\\Windows\\fonts\\Verdana.ttf', 11)
    body_font = ImageFont.truetype('C:\\Windows\\fonts\\Verdana.ttf', 13)
    width = 700
    margin = 8
    score_height = 20
    # TODO: figure out offset instead of a magic constant
    text_offset = 36
    text = process_text(comment.body, width, body_font, margin, icon)
    text_height = get_text_height(text, body_font)
    height = text_height + text_offset + icon.height + margin
    # height = text_height + text_offset + score_height + icon.height + margin

    image = Image.new(mode='RGB', size=(width, height), color=ImageColor.getrgb('#1A1A1B'))
    mask_image = get_mask(icon, save_path)
    draw = ImageDraw.Draw(image)
    
    header_y = (2 * margin + icon.height) / 2 - (header_font.getbbox(username)[3] / 2)
    draw.text((2 * margin + icon.width, header_y), username, fill=(255, 255, 255), font=header_font)

    # TODO: figure out how to draw text without offset
    draw.multiline_text((2 * margin + icon.width, icon.height), text, fill=(255,255,255), font=body_font)

    line_x1 = (2 * margin + icon.width) / 2
    line_x2 = line_x1
    line_y1 = 2 * margin + icon.height
    line_y2 = height
    line_coords1 = (line_x1, line_y1)
    line_coords2 = (line_x2, line_y2)
    draw.line([line_coords1, line_coords2], fill=(52, 53, 54), width=2)

    base_image = image.copy()
    base_image.paste(icon, (margin, margin, icon.width + margin, icon.height + margin), mask_image)

    base_image.save(os.path.join(save_path, file_name), 'PNG')

# TODO: finish this
def generate_submission_picture():
    True

def generate_pictures(submission_id, comments, save_path):
    i = 1
    generate_submission_picture()
    i += 1

    for comment in comments:
        index = text_to_speech.file.get_file_name(comments, i, 'image', '.png')[1]
        file_name = text_to_speech.file.get_file_name(comments, i, 'image', '.png')[0]
        generate_comment_picture(comment, save_path, file_name, index)
        i += 1

# comment = config.REDDIT_CLIENT.comment(id='jbwucnw')
# save_path = 'media\\AskReddit\\11p9o5i'
# # save_path = 'D:\\coding\\Python\\python-reddit-tts\\media\\AskReddit\\11p9o5i'

# generate_picture(comment, save_path)