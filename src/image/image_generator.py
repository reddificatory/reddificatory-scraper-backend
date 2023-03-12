import os
import sys
sys.path.insert(0, os.getcwd() + '/src')
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageColor
import config
import urllib.request

def get_profile_pic(author, save_path):
    path = os.path.join(save_path, 'icon.png')

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

def generate_picture(comment, save_path):
    author = comment.author
    icon = get_profile_pic(author, save_path)
    username = author.name
    body = comment.body
    score = comment.score

    width = 700
    height = 1000
    margin = 8

    image = Image.new(mode='RGB', size=(width, height), color=ImageColor.getrgb('#1A1A1B'))
    mask_image = get_mask(icon, save_path)
    draw = ImageDraw.Draw(image)

    base_image = image.copy()
    base_image.paste(icon, (margin, margin, icon.width + margin, icon.height + margin), mask_image)

    base_image.save(os.path.join(save_path, 'image.png'), 'PNG')
    image.save(os.path.join(save_path, 'image2.png'), 'PNG')

comment = config.REDDIT_CLIENT.comment(id='jbwucnw')
save_path = 'media\\AskReddit\\11p9o5i'
# save_path = 'D:\\coding\\Python\\python-reddit-tts\\media\\AskReddit\\11p9o5i'

generate_picture(comment, save_path)