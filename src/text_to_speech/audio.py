import os
import sys
sys.path.insert(0, os.getcwd() + '/src')

import glob

def get_audio_file_names(save_path):
    path = os.path.join(os.getcwd(), save_path)

    print(path)

get_audio_file_names('asd')
