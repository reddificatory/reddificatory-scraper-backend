import pysrt

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

    return durations

def generate_subtitle(text, max_line_length, rate):
    subtitle_file = pysrt.SubRipFile()
    lines = process_text(text, max_line_length);
    durations = get_durations(lines, rate)

    for i in range(len(lines)):
        subtitle_file.append(pysrt.SubRipItem(index = i + 1, start = durations[i][0], end = durations[i][1], text = lines[i]))

    subtitle_file.save('./output.srt')
    return subtitle_file