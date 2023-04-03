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

# def get_profile_pic(author, save_path, index):
#     file_name = f'icon{index}.png'
#     path = os.path.join(save_path, file_name)

#     if not os.path.exists(path):
#         # TODO: Exception has occurred: AttributeError 'Redditor' object has no attribute 'icon_img'
#         urllib.request.urlretrieve(author.icon_img, path)
#         icon_image = Image.open(path)
#         icon_image.thumbnail((50, 50))
#         icon_image.save(path)

#     return Image.open(path)

# def get_mask(image, save_path):
#     path = os.path.join(save_path, 'mask.png')

#     # if not os.path.exists:
#     mask_image = Image.new('L', image.size, 0)
#     draw = ImageDraw.Draw(mask_image)
#     draw.ellipse((0, 0, image.size[0] - 1, image.size[1] - 1), 255)
#     mask_image = mask_image.filter(ImageFilter.GaussianBlur(0.6))
#     mask_image.save(path)

#     return Image.open(path)

# # TODO: get rid of empty lines
# def generate_comment_image(comment, save_path, file_name, index):
#     author = comment.author
#     icon = get_profile_pic(author, save_path, index)
#     username = author.name
#     body = comment.body
#     score = comment.score
    
#     header_font = ImageFont.truetype('C:\\Windows\\fonts\\Verdana.ttf', 26)
#     body_font = ImageFont.truetype('C:\\Windows\\fonts\\Verdana.ttf', 28)
#     width = 950
#     margin = 8
#     score_height = 20
#     # TODO: figure out offset instead of a magic constant
#     text_offset = 36
#     text = image_generator.text.process_text(body, width, body_font, margin, icon)
#     text_height = image_generator.text.get_text_height(text, body_font)
#     height = text_height + text_offset + icon.height + margin
#     # height = text_height + text_offset + score_height + icon.height + margin

#     image = Image.new(mode='RGBA', size=(width, height), color=ImageColor.getrgb('#1A1A1B'))
#     mask_image = get_mask(icon, save_path)
#     draw = ImageDraw.Draw(image)
    
#     header_y = (2 * margin + icon.height) / 2 - (header_font.getbbox(username)[3] / 2)
#     draw.text((2 * margin + icon.width, header_y), username, fill=(255, 255, 255), font=header_font)

#     # TODO: figure out how to draw text without offset
#     draw.multiline_text((2 * margin + icon.width, icon.height), text, fill=(255,255,255), font=body_font)

#     line_x1 = (2 * margin + icon.width) / 2
#     line_x2 = line_x1
#     line_y1 = 2 * margin + icon.height
#     line_y2 = height
#     line_coords1 = (line_x1, line_y1)
#     line_coords2 = (line_x2, line_y2)
#     draw.line([line_coords1, line_coords2], fill=(52, 53, 54), width=2)

#     base_image = image.copy()
#     base_image.paste(icon, (margin, margin, icon.width + margin, icon.height + margin), mask_image)

#     base_image.save(os.path.join(save_path, file_name), 'PNG')

# # TODO: finish this
# def generate_submission_image(submission_id, save_path, file_name):
#     submission = config.REDDIT_CLIENT.submission(submission_id)
#     author = submission.author
#     username = author.name
#     title = submission.title
#     score = submission.score

#     header_font = ImageFont.truetype('C:\\Windows\\fonts\\Verdana.ttf', 26)
#     title_font = ImageFont.truetype('C:\\Windows\\fonts\\Verdana.ttf', 31)
#     width = 950
#     margin = 8
#     text_offset = 36
#     header = f'@askredditts.x • r/{submission.subreddit.display_name} • Follow for more content!'
#     header_height = image_generator.text.get_text_height(header, header_font)
#     text = image_generator.text.process_text(title, width, title_font, margin)
#     text_height = image_generator.text.get_text_height(text, title_font)
#     height = 3 * margin + header_height + text_height + text_offset

#     image = Image.new(mode='RGB', size=(width, height), color=ImageColor.getrgb('#1A1A1B'))
#     draw = ImageDraw.Draw(image)

#     draw.text((margin, margin), header, fill=(255, 255, 255), font=header_font)
#     draw.multiline_text((margin , margin + header_height), text, fill=(255,255,255), font=title_font)

#     image.save(os.path.join(save_path, file_name), 'PNG')

# def generate_images(submission_id, comments, save_path):
#     image_list_file = open(os.path.join(save_path, 'images.txt'), 'w', encoding='UTF-8')
#     image_file_name = file.get_file_name(comments, 0, 'image', '.png')[0]
#     audio_file_name = file.get_file_name(comments, 0, 'audio', '.wav')[0]

#     print('Generating submission image...')
#     generate_submission_image(submission_id, save_path, image_file_name)
#     print(f'Saved submission image to {os.path.join(save_path, image_file_name)}')
#     image_list_file.write(f'file {image_file_name}\n')
#     image_list_file.write(f'outpoint {librosa.get_duration(path=os.path.join(save_path, audio_file_name))}\n')
    
#     print('Generating comment images...')
#     i = 1
#     for comment in comments:
#         index = file.get_file_name(comments, i, 'image', '.png')[1]
#         image_file_name = file.get_file_name(comments, i, 'image', '.png')[0]
#         audio_file_name = file.get_file_name(comments, i, 'audio', '.wav')[0]
#         generate_comment_image(comment, save_path, image_file_name, index)
#         image_list_file.write(f'file {image_file_name}\n')
#         image_list_file.write(f'outpoint {librosa.get_duration(path=os.path.join(save_path, audio_file_name))}\n')
#         i += 1

#     path = os.path.join(save_path, 'images*.png')
#     print(f'Saved submission image to {path}')
#     image_list_file.close()

#     max_height = max_image_height(save_path)
#     image_files = get_image_files(save_path)

#     print('Resizing images...')
#     for image_file in image_files:
#         resize_image(image_file, max_height)
#     print('Images resized')


# def merge_images():
#     # print(os.getcwd())
#     # media_path = os.path.join(os.getcwd(), save_path)
#     # media_path = os.path.join(save_path)
#     # os.chdir(media_path)
#     # os.system('ffmpeg -f concat -i images.txt merged.mp4')
#     os.system('ffmpeg -f concat -i images.txt merged.mp4')

# def max_image_height(save_path):
#     image_paths = glob.glob(os.path.join(save_path, 'image*.png'))
#     max_height = Image.open(image_paths[0]).size[1]

#     for image_path in image_paths:
#         image_height = Image.open(image_path).size[1]
        
#         if image_height > max_height:
#             max_height = image_height

#     return max_height

# def get_image_files(save_path):
#     return glob.glob(os.path.join(save_path, 'image*.png'))

# def resize_image(file_name, height):
#     width = 950
#     image = Image.open(file_name)
#     blank_image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
#     y = int(round((height - image.size[1]) / 2, 0))

#     blank_image.paste(image, (0, y))
#     blank_image.save(file_name)

def get_text_height(text, font):
    bbox_draw = ImageDraw.Draw(Image.new('RGB', (0, 0)))
    bbox = bbox_draw.textbbox((0, 0), text, font) # left, top, right, bottom
    #print(bbox[3])
    return bbox[3]

def draw_submission(submission, save_path, file_name, title=False, body=False):
    if not title and not body:
        return 0
    
    # TODO: make font available independent of OS
    header_font = ImageFont.truetype('C:\\Windows\\fonts\\Verdana.ttf', 18)
    title_font = ImageFont.truetype('C:\\Windows\\fonts\\Verdana.ttf', 30) 
    body_font = ImageFont.truetype('C:\\Windows\\fonts\\Verdana.ttf', 22) 
    
    padding = 8
    image_width = 900
    image_height = 2 * padding
    
    header = f'@askredditts.x • r/{submission.subreddit.display_name} • Follow for more content!'
    #header = 'Lines for the\nheader of the image'
    wrapped_header = text_processor.wrap_text(header, image_width - 2 * padding, header_font)
    wrapped_title = ''
    wrapped_body = ''
    
    header_height = get_text_height(wrapped_header, header_font)
    title_height = 0
    body_height = 0

    image_height += header_height
    if title:
        wrapped_title = text_processor.wrap_text(submission.title, image_width - 2 * padding, title_font)
        #wrapped_title = 'Lines for the\ntitle of the image'
        title_height = get_text_height(wrapped_title, title_font)
        image_height += title_height + padding    
    if body:        
        wrapped_body = text_processor.wrap_text(submission.selftext, image_width - 2 * padding, body_font)
        #wrapped_body = '[Line]\'"s for the\nbody of the image'
        body_height = get_text_height(wrapped_body, body_font)
        image_height += body_height + padding
    
    background_color = ImageColor.getrgb('#1A1A1B')
    image = Image.new('RGB', (image_width, image_height), background_color)
    draw = ImageDraw.Draw(image)    
    x = padding
    # y = padding 
    y = 0

    y1 = y
    y2 = y1 + padding

    draw.rectangle(((0, 0), (padding, image_height)), fill='green')
    draw.rectangle(((image_width - padding, 0), (image_width, image_height)), fill='green')

    draw.multiline_text((x, y), wrapped_header, font=header_font)
    draw.rectangle(((x, y1), (image_width - x, y2)), fill='red')
    y += header_height

    y1 = y
    y2 = y1 + padding
    draw.rectangle(((x, y1), (image_width - x, y2)), fill='red')
    if title:
        # y += padding
        print(wrapped_title)
        draw.multiline_text((x, y), wrapped_title, font=title_font)
        y += title_height

        y1 = y
        y2 = y1 + padding
        draw.rectangle(((x, y1), (image_width - x, y2)), fill='red')
    if body:
        # y += padding
        print(submission.selftext)
        print(wrapped_body)
        draw.multiline_text((x, y), wrapped_body, font=body_font)
        y += body_height

        y1 = y
        y2 = y1 + padding
        draw.rectangle(((x, y1), (image_width - x, y2)), fill='red')

    image.show()

def draw_comment(text, save_path, file_name):
    print(file_name)

def run(submission, save_path, title=True, body=False, comments=False):
    list_length = 0
    index = 0
    if comments:
        list_length += len(comments)

    if title or body:
        list_length += 1
        file_name = f'image{file.get_index(list_length, index)}.png'
        draw_submission(submission, save_path, file_name, title, body)
        index += 1

    if comments:
        while index < len(comments):
            file_name = f'image{file.get_index(list_length, index)}.png'    
            draw_comment(text_processor.remove_duplicate_newlines(comments[index]), save_path, file_name)
            #print(text_processor.remove_duplicate_newlines(comments[index]))
            index += 1

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