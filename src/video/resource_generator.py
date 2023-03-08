import sys
sys.path.insert(0, 'D:\coding\Python\python-reddit-tts\src')

# import subtitle.subtitle_generator
import text_to_speech.tts

random_submission_id = text_to_speech.tts.get_random_submission('askreddit')
save_path = text_to_speech.tts.get_save_path(random_submission_id)
max_line_length = 40
wpm_rate = 155
tts_engine = text_to_speech.tts.config_engine(wpm_rate)

lines = text_to_speech.tts.save(random_submission_id, tts_engine, max_line_length)
# subtitle.subtitle_generator.generate_subtitle(lines, save_path)