import sys
sys.path.insert(0, 'D:\coding\python-reddit-tts\src')

import pysrt
import config
import tts.tts

def process_text(text, max_line_length):
    lines = []
    line = ""

    for word in text.split():
        if len(line) + len(word) + 1 <= max_line_length:
            line += f" {word}"
        else:
            lines.append(line.strip())            
            line = word

    if line:
        lines.append(line.strip())

    return lines

def get_durations(lines, rate):
    durations = []
    start_time = pysrt.SubRipTime()
    
    for line in lines:
        end_time = int(len(line) / (rate / 60.0) * 1000)
        end_time = start_time + pysrt.SubRipTime(milliseconds=end_time)
        
        durations.append([start_time, end_time])
        
        start_time = end_time

def generate_subtitle(text, max_line_length):
    for line in process_text(text, max_line_length):
        print(line)
    #process_text(text, max_line_length)
    return 0


# generate_subtitle('buzi geci faszom kivan mar nem ertek semmit kezdem megkerdojelezni minden dontesem elegem van ebbol a szaros geci faszom mindenbol istenem konyorgom h segits meg engem', 40)

get_durations(process_text('buzi geci faszom kivan mar nem ertek semmit kezdem megkerdojelezni minden dontesem elegem van ebbol a szaros geci faszom mindenbol istenem konyorgom h segits meg engem', 40), 160)