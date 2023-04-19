import os
import librosa

def merge_audios(save_path):
    current_directory = os.getcwd()
    save_path = os.path.join(current_directory, save_path)
    os.chdir(save_path)
    os.system('ffmpeg -f concat -i audios.txt merged.wav')
    os.chdir(current_directory)

def get_duration(path):
    return librosa.get_duration(path=path)