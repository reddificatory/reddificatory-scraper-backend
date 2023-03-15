import os
import sys
sys.path.insert(0, os.getcwd() + '/src')

import text_to_speech.speech
import text_to_speech.file
import text_to_speech.text
import text_to_speech.audio
import images.image_generator

max_line_length = 40
wpm_rate = 155
comment_count = 3
random_submission_id = text_to_speech.text.get_random_submission('askreddit')
# random_submission_id = '11okj6g'
save_path = text_to_speech.file.get_save_path(random_submission_id)
comments = text_to_speech.text.get_comments(random_submission_id, 2)
tts_engine = text_to_speech.speech.config_engine(wpm_rate)
durations = text_to_speech.audio.get_durations(save_path)

text_to_speech.speech.save(random_submission_id, tts_engine, comments)
images.image_generator.generate_images(random_submission_id, comments, save_path)
text_to_speech.audio.merge_audios(save_path)
images.image_generator.merge_images(save_path)