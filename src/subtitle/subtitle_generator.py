import pysrt
import librosa
import glob
import os

def get_durations(save_path):
    durations = []
    start_time = pysrt.SubRipTime()
    
    # for i, line in enumerate(lines):
    #     # start_time = pysrt.SubRipTime()
    #     # end_time = pysrt.SubRipTime(milliseconds=durations[i]) + start_time
        
    #     # durations.append([start_time, end_time])
    #     # print(f'{start_time} {end_time}')
        
    #     # start_time = end_time
    #     print(i)
    #     print(line)

    filenames = glob.glob(os.path.join(save_path, '*.wav'))
    for filename in filenames:
        print(filename)

    return durations

def generate_subtitle(lines, save_path):
    subtitle_file = pysrt.SubRipFile()
    durations = get_durations(lines)

    # for i in range(len(lines)):
    #     subtitle_file.append(pysrt.SubRipItem(index = i + 1, start = durations[i][0], end = durations[i][1], text = lines[i]))

    # subtitle_file.save(f'{save_path}/subtitles.srt')
    return subtitle_file

# TODO: finish getting the durations
get_durations('videos/AskReddit/11lm6q5')