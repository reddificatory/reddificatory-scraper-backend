import os
import sys
sys.path.insert(0, os.getcwd() + '/src')

import librosa
import glob

def merge_audios(save_path):
    media_path = os.path.join(os.getcwd(), save_path)
    os.chdir(media_path)
    os.system('ffmpeg -f concat -i audios.txt merged.wav')

def get_duration(path):
    return librosa.get_duration(path=path)

# def get_durations(save_path):
#     media_path = os.path.join(os.getcwd(), save_path)
#     audio_paths = glob.glob(os.path.join(media_path, 'audio*.wav'))
#     durations = []

#     for audio_path in audio_paths:
#         durations.append(librosa.get_duration(path=audio_path))

#     return durations
