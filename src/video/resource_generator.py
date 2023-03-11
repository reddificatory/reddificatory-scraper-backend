import os
import sys
sys.path.insert(0, os.getcwd() + '/src')

import text_to_speech.speech
import text_to_speech.file
import text_to_speech.text

random_submission_id = text_to_speech.text.get_random_submission('askreddit')
save_path = text_to_speech.file.get_save_path(random_submission_id)
lines = text_to_speech.text.get_lines(random_submission_id, 3)
max_line_length = 40
wpm_rate = 155
comment_count = 3
tts_engine = text_to_speech.speech.config_engine(wpm_rate)

text_to_speech.speech.save(random_submission_id, tts_engine, lines)