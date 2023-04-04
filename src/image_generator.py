import os
import sys
sys.path.insert(0, os.getcwd() + '/src')
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageColor
import urllib.request
import file
# import audio
import config
import glob
import text_processor
import file

def get_icon(redditor, save_path, file_index, image_width):
    file_name = f'icon{file_index}.png'
    path = os.path.join(save_path, file_name)

    if not os.path.exists(path):
        # TODO: Exception has occurred: AttributeError 'Redditor' object has no attribute 'icon_img'
        urllib.request.urlretrieve(redditor.icon_img, path)
        icon_image = Image.open(path)

        icon_image.thumbnail((int(image_width * 0.06), int(image_width * 0.06)))

        icon_image.save(path)

    return Image.open(path)

def get_mask(image, save_path):
    path = os.path.join(save_path, 'mask.png')
    mask_image = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask_image)

    draw.ellipse((0, 0, image.size[0] - 1, image.size[1] - 1), 255)
    mask_image = mask_image.filter(ImageFilter.GaussianBlur(0.62))

    mask_image.save(path)
    return Image.open(path)

# def merge_images():
#     # print(os.getcwd())
#     # media_path = os.path.join(os.getcwd(), save_path)
#     # media_path = os.path.join(save_path)
#     # os.chdir(media_path)
#     # os.system('ffmpeg -f concat -i images.txt merged.mp4')
#     os.system('ffmpeg -f concat -i images.txt merged.mp4')

def get_max_image_height(image_files):
    max_height = Image.open(image_files[0]).size[1]
    for image_file in image_files:
        image_height = Image.open(image_file).size[1]
        
        if image_height > max_height:
            max_height = image_height

    return max_height

def get_image_files(path):
    return glob.glob(os.path.join(path, 'image*.png'))

def resize_image(file_name, height):
    image = Image.open(file_name)
    blank_image = Image.new('RGBA', (image.width, height), (0, 0, 0, 0))

    y = int(round((height - image.size[1]) / 2, 0))    
    blank_image.paste(image, (0, y))

    blank_image.save(file_name)

def get_text_height(text, font):
    bbox_draw = ImageDraw.Draw(Image.new('RGB', (0, 0)))
    bbox = bbox_draw.textbbox((0, 0), text, font) # left, top, right, bottom
    
    return bbox[3]

def draw_submission(submission, save_path, file_name, title=False, body=False):
    if not title and not body:
        return 0
    
    # TODO: make font available independent of OS
    header_font = ImageFont.truetype('C:\\Windows\\fonts\\Verdana.ttf', 18)
    title_font = ImageFont.truetype('C:\\Windows\\fonts\\Verdana.ttf', 30) 
    body_font = ImageFont.truetype('C:\\Windows\\fonts\\Verdana.ttf', 22) 
    
    padding = 16
    image_width = 900
    max_width = image_width - 2 * padding
    image_height = 2 * padding
    
    header = f'@askredditts.x • r/{submission.subreddit.display_name} • Follow for more content!'
    wrapped_header = text_processor.wrap_text(header, max_width, header_font)
    wrapped_title = ''
    wrapped_body = ''
    
    header_height = get_text_height(wrapped_header, header_font)
    title_height = 0
    body_height = 0

    image_height += header_height
    if title:
        wrapped_title = text_processor.wrap_text(submission.title, max_width, title_font)
        title_height = get_text_height(wrapped_title, title_font)
        image_height += title_height + padding    
    if body:        
        wrapped_body = text_processor.wrap_text(submission.selftext, max_width, body_font)
        body_height = get_text_height(wrapped_body, body_font)
        image_height += body_height + padding
    
    background_color = ImageColor.getrgb('#1A1A1B')
    image = Image.new('RGB', (image_width, image_height), background_color)
    draw = ImageDraw.Draw(image)    
    x = padding
    y = padding

    draw.multiline_text((x, y), wrapped_header, font=header_font)
    y += header_height + padding

    if title:
        draw.multiline_text((x, y), wrapped_title, font=title_font)
        y += title_height + padding
    if body:
        draw.multiline_text((x, y), wrapped_body, font=body_font)
        y += body_height + padding

    image.save(os.path.join(save_path, file_name), 'PNG')

def draw_comment(comment, save_path, file_index, file_name):
    username_font = ImageFont.truetype('C:\\Windows\\fonts\\Verdana.ttf', 26)
    body_font = ImageFont.truetype('C:\\Windows\\fonts\\Verdana.ttf', 28)

    padding = 16
    image_width = 900
    icon = get_icon(comment.author, save_path, file_index, image_width)
    icon_mask = get_mask(icon, save_path)
    max_width = image_width - (3 * padding + icon.width)
    image_height = 3 * padding + icon.height
    
    wrapped_username = text_processor.wrap_text(comment.author.name, max_width, username_font)
    wrapped_body = text_processor.wrap_text(comment.body, max_width, body_font)
    
    username_height = get_text_height(wrapped_username, username_font)
    body_height = get_text_height(wrapped_body, body_font)

    # image_height += username_height + padding + body_height
    image_height += body_height

    background_color = ImageColor.getrgb('#1A1A1B')
    image = Image.new('RGB', (image_width, image_height), background_color)
    x = padding
    y = padding   

    base_image = image.copy()
    draw = ImageDraw.Draw(base_image)

    base_image.paste(icon, (x, y, icon.width + x, icon.height + y), icon_mask)    
    draw.line(((padding + icon.width / 2, 2 * padding + icon.height), (padding + icon.width / 2, image_height - padding)), fill=(52, 53, 54), width=3)

    draw.multiline_text((icon.width + 2 * padding, icon.height / 2 + padding - username_height / 2), wrapped_username, font=username_font)
    # bbox = draw.textbbox((icon.width + 2 * padding, icon.height / 2 + padding - username_height / 2), wrapped_username, font=username_font)
    # draw.rectangle(bbox, outline='red')

    draw.multiline_text((icon.width + 2 * padding, icon.height + 2 * padding), wrapped_body, font=body_font)
    # bbox = draw.textbbox((icon.width + 2 * padding, 2 * padding + icon.height), wrapped_body, font=body_font)
    # draw.rectangle(bbox, outline='green')

    base_image.save(os.path.join(save_path, file_name), 'PNG')

def run(submission, save_path, title=False, body=False, comments=False):
    list_length = 0
    index = 0
    difference = 0
    if comments:
        list_length += len(comments)

    if title or body:
        list_length += 1
        file_index = file.get_index(list_length, index)
        file_name = f'image{file_index}.png'
        draw_submission(submission, save_path, file_name, title, body)
        index += 1
        difference += 1

    if comments:
        while index < len(comments) + difference:
            file_index = file.get_index(list_length, index)
            file_name = f'image{file_index}.png'
            draw_comment(comments[index - difference], save_path, file_index, file_name)
            index += 1

    image_files = get_image_files(save_path)
    max_image_height = get_max_image_height(image_files)
    for image_file in image_files:
        resize_image(image_file, max_image_height)