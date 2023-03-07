import sys
sys.path.insert(0, 'D:\coding\python-reddit-tts\src')

import subtitle.subtitle_generator
import text_to_speech.tts

random_submission_id = text_to_speech.tts.get_random_submission('askreddit')
save_path = text_to_speech.tts.get_save_path(random_submission_id)
wpm_rate = 160
tts_engine = text_to_speech.tts.config_engine(wpm_rate)

text = text_to_speech.tts.save(random_submission_id, tts_engine)
subtitle.subtitle_generator.generate_subtitle(text, 60, wpm_rate, save_path)