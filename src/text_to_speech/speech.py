import os
import sys
sys.path.insert(0, os.getcwd() + '/src')
import pyttsx3
import text_to_speech.file
import text_to_speech.text
import config

def config_engine(rate):
    tts = pyttsx3.init()
    tts.setProperty('rate', rate)
    tts.setProperty('volume', 1)

    print('TTS config done...')

    return tts

def save(submission_id, tts, comments):
    submission = config.REDDIT_CLIENT.submission(submission_id)
    title = submission.title
    save_path = text_to_speech.file.get_save_path(submission_id)
    audio_list_file = open(os.path.join(save_path, 'audios.txt'), 'w', encoding='UTF-8')
    file_name = 'audio'
    file_extension = '.wav'

    print('Saving text-to-speech line-by-line output...')

    i = 0
    audio_file_name = text_to_speech.file.get_file_name(comments, i, file_name, file_extension)[0]
    tts.save_to_file(title, f'{save_path}\\{audio_file_name}')
    audio_list_file.write(f'file {audio_file_name}\n')

    for comment in comments:
        i += 1
        audio_file_name = text_to_speech.file.get_file_name(comments, i, file_name, file_extension)[0]
        tts.save_to_file(comment.body, f'{save_path}\\{audio_file_name}')
        audio_list_file.write(f'file {audio_file_name}\n')

    print(f'Saved text-to-speech line-by-line output to {save_path}\\audio*.wav ({len(comments) + 1} files saved)')

    tts.runAndWait()
    audio_list_file.close()