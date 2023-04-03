import os
import sys
sys.path.insert(0, os.getcwd() + '/src')
import text_to_speech.speech
import file
import text_to_speech.text
import audio
import image_generator
import video_generator.video

max_line_length = 40
wpm_rate = 155
comment_count = 3
random_submission_id = text_to_speech.text.get_random_submission('askreddit')
# random_submission_id = '11okj6g'
save_path = file.get_save_path(random_submission_id)
video_file_name = 'merged.mp4'
comments = text_to_speech.text.get_comments(random_submission_id, 2)
tts_engine = text_to_speech.speech.config_engine(wpm_rate)
#durations = text_to_speech.audio.get_durations(save_path)

#get_gameplay_section(save_path)

text_to_speech.speech.save(random_submission_id, tts_engine, comments)
image_generator.generate_images(random_submission_id, comments, save_path)
audio.merge_audios(save_path)
image_generator.merge_images()

gameplay_durations = video_generator.video.get_gameplay_duration()
#print(videos.video.get_video_duration(video_file_name))
video_generator.video.get_gameplay_section(video_generator.video.get_random_gameplay(), gameplay_durations[0], gameplay_durations[1])
video_generator.video.get_merged_video()