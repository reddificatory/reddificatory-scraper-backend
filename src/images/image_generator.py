import os
import sys
sys.path.insert(0, os.getcwd() + '/src')
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageColor
import urllib.request
import text_to_speech.file
import text_to_speech.audio
import config
import images.text
import librosa
import glob

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

def generate_comment_image(comment, save_path, file_name, index):
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
    text = images.text.process_text(body, width, body_font, margin, icon)
    text_height = images.text.get_text_height(text, body_font)
    height = text_height + text_offset + icon.height + margin
    # height = text_height + text_offset + score_height + icon.height + margin

    image = Image.new(mode='RGBA', size=(width, height), color=ImageColor.getrgb('#1A1A1B'))
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
def generate_submission_image(submission_id, save_path, file_name):
    submission = config.REDDIT_CLIENT.submission(submission_id)
    author = submission.author
    username = author.name
    title = submission.title
    score = submission.score

    header_font = ImageFont.truetype('C:\\Windows\\fonts\\Verdana.ttf', 11)
    title_font = ImageFont.truetype('C:\\Windows\\fonts\\Verdana.ttf', 16)
    width = 700
    margin = 8
    text_offset = 36
    header = f'@askredditts.x • r/{submission.subreddit.display_name} • Follow for more content!'
    header_height = images.text.get_text_height(header, header_font)
    text = images.text.process_text(title, width, title_font, margin)
    text_height = images.text.get_text_height(text, title_font)
    height = 3 * margin + header_height + text_height + text_offset

    image = Image.new(mode='RGB', size=(width, height), color=ImageColor.getrgb('#1A1A1B'))
    draw = ImageDraw.Draw(image)

    draw.text((margin, margin), header, fill=(255, 255, 255), font=header_font)
    draw.multiline_text((margin , margin + header_height), text, fill=(255,255,255), font=title_font)

    image.save(os.path.join(save_path, file_name), 'PNG')

def generate_images(submission_id, comments, save_path):
    image_list_file = open(os.path.join(save_path, 'images.txt'), 'w', encoding='UTF-8')
    image_file_name = text_to_speech.file.get_file_name(comments, 0, 'image', '.png')[0]
    audio_file_name = text_to_speech.file.get_file_name(comments, 0, 'audio', '.wav')[0]

    print('Generating submission image...')
    generate_submission_image(submission_id, save_path, image_file_name)
    print(f'Saved submission image to {os.path.join(save_path, image_file_name)}')
    image_list_file.write(f'file {image_file_name}\n')
    image_list_file.write(f'outpoint {librosa.get_duration(path=os.path.join(save_path, audio_file_name))}\n')
    
    print('Generating comment images...')
    i = 1
    for comment in comments:
        index = text_to_speech.file.get_file_name(comments, i, 'image', '.png')[1]
        image_file_name = text_to_speech.file.get_file_name(comments, i, 'image', '.png')[0]
        audio_file_name = text_to_speech.file.get_file_name(comments, i, 'audio', '.wav')[0]
        generate_comment_image(comment, save_path, image_file_name, index)
        image_list_file.write(f'file {image_file_name}\n')
        image_list_file.write(f'outpoint {librosa.get_duration(path=os.path.join(save_path, audio_file_name))}\n')
        i += 1

    path = os.path.join(save_path, 'images*.png')
    print(f'Saved submission image to {path}')
    image_list_file.close()

    max_height = max_image_height(save_path)
    image_files = get_image_files(save_path)

    print('Resizing images...')
    for image_file in image_files:
        resize_image(image_file, max_height)
    print('Images resized')


def merge_images(save_path):
    # print(os.getcwd())
    media_path = os.path.join(os.getcwd(), save_path)
    # media_path = os.path.join(save_path)
    # os.chdir(media_path)
    os.system('ffmpeg -f concat -i images.txt merged.mp4')

def max_image_height(save_path):
    image_paths = glob.glob(os.path.join(save_path, 'image*.png'))
    max_height = Image.open(image_paths[0]).size[1]

    for image_path in image_paths:
        image_height = Image.open(image_path).size[1]
        
        if image_height > max_height:
            max_height = image_height

    return max_height

def get_image_files(save_path):
    return glob.glob(os.path.join(save_path, 'image*.png'))

def resize_image(file_name, height):
    width = 700
    image = Image.open(file_name)
    blank_image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    y = int(round((height - image.size[1]) / 2, 0))

    blank_image.paste(image, (0, y))
    blank_image.save(file_name)

# # comment = config.REDDIT_CLIENT.comment(id='jbwucnw')
# save_path = 'media\\AskReddit\\11pk6qu'
# max_height = max_image_height(save_path)
# # durations = text_to_speech.audio.get_durations(save_path)
# # submission_id = '11pfqs6'
# # file_name = 'image01.png'
# # # # save_path = 'D:\\coding\\Python\\python-reddit-tts\\media\\AskReddit\\11p9o5i'

# # generate_submission_picture(submission_id, save_path, file_name)

# # merge_images(save_path)
# resize_image(save_path, 'image3.png', 200)