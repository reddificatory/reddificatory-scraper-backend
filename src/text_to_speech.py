import os
import sys
sys.path.insert(0, os.getcwd() + '/src')
import pyttsx3
import config
import file

def config_engine(rate):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.setProperty('volume', 1)

    print('TTS config done...')

    return engine

def run(texts, save_path, engine):
    audio_list_file = open(os.path.join(save_path, 'audios.txt'), 'w', encoding='UTF-8')

    print('Saving TTS output...')
    for i, text in enumerate(texts):
        file_name = f'audio{file.get_index(len(texts), i)}.wav'
        engine.save_to_file(text, os.path.join(save_path, file_name))
        audio_list_file.write(f'file {file_name}\n')

    engine.runAndWait()
    audio_list_file.close()
    print(f'TTS output saved to {save_path}')

run(['asd', 'asd', 'asd', 'asd', 'asd', 'asd', 'asd', 'asd', 'asd', 'asd', 'asd', 'asd', 'asd', 'asd', 'asd'], file.get_save_path(os.path.join('media', 'reddit'), "123ohqw"), config_engine(150))