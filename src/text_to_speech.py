import os
import sys
sys.path.insert(0, os.getcwd() + '/src')
import pyttsx3
import config
import file
import logger

def config_engine(rate):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.setProperty('volume', 1)
    logger.logger.debug('TTS configurated.')
    return engine

def run(texts, save_path, engine):
    audio_list_file = open(os.path.join(save_path, 'audios.txt'), 'w', encoding='UTF-8')

    logger.logger.debug('Saving TTS output...')
    for i, text in enumerate(texts):
        file_name = f'audio{file.get_index(len(texts), i)}.wav'
        engine.save_to_file(text, os.path.join(save_path, file_name))
        audio_list_file.write(f'file {file_name}\n')

    engine.runAndWait()
    audio_list_file.close()
    logger.logger.debug(f'TTS output saved to {save_path}')