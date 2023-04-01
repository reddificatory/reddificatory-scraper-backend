import subprocess
import os
import glob
import random

def get_video_duration(file_name):
    print(os.getcwd(), file_name)
    return float(subprocess.check_output(f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{file_name}"').decode())

def get_random_gameplay():
    #print(os.getcwd(), glob.glob(os.path.join('..', '..', '..', 'gameplays', '*')))
    gameplays = glob.glob(os.path.join('..', '..', '..', 'gameplays', '*'))
    random_index = random.randint(1, len(gameplays)) - 1
    return gameplays[random_index]

def get_gameplay_duration():
    gameplay = get_random_gameplay()
    gameplay_duration = get_video_duration(gameplay)
    image_video = 'merged.mp4'
    image_video_duration = get_video_duration(image_video)

    random_start_time = random.uniform(1, gameplay_duration) - 1
    random_end_time = random_start_time + image_video_duration

    while random_end_time > gameplay_duration:
        random_start_time = random.uniform(1, gameplay_duration) - 1
        random_end_time = random_start_time + image_video_duration

    return random_start_time, random_end_time

def get_sexagesimal_time(seconds):
    total_seconds, fractional_seconds = divmod(seconds, 1)
    hours, remaining_seconds = divmod(int(total_seconds), 3600)
    minutes, seconds = divmod(remaining_seconds, 60)
    sexagesimal_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{int(fractional_seconds * 1000):03d}"
    return sexagesimal_time

def get_gameplay_section(gameplay, start_time, end_time):
    # output_path = os.path.join(save_path, 'gameplay.mp4')
    command = f'ffmpeg -ss {get_sexagesimal_time(start_time)} -to {get_sexagesimal_time(end_time)} -i "{gameplay}" -filter_complex "[0:v]crop=ih*(9/16):ih[cropped]" -map [cropped] gameplay.mp4'
    os.system(command)
    print(command)

def get_merged_video():
    #path = os.path.join(os.getcwd(), save_path)
    #os.chdir(path)    
    #command = f'ffmpeg -i gameplay.mp4 -i merged.mp4 -i merged.wav -filter_complex "[0:v]crop=ih*(9/16):ih[backgr];[1:v]scale=-2:-2[ovrl];[backgr][ovrl]overlay=(W-w)/2:(H-h)/2[outv]" -map [outv] -map 2:a -shortest video.mp4'
    #command = f'ffmpeg -i gameplay.mp4 -i merged.mp4 -i merged.wav -filter_complex "[1:v]scale=-2:-2[ovrl];[0:v][ovrl]overlay=(W-w)/2:(H-h)/2[outv]" -map [outv] -map 2:a video.mp4'

    # TODO: get scaling right finally
    command = f'ffmpeg -i gameplay.mp4 -i merged.mp4 -i merged.wav -filter_complex "[1:v][0:v]scale2ref=\'oh*mdar\':\'ih*mdar\'[ovrl][backgr];[backgr][ovrl]overlay=(W-w)/2:(H-h)/2[outv]" -map [outv] -map 2:a video.mp4'

    os.system(command)

# save_path = 'media\\reddit\\AskReddit\\11qjtjy'
# gameplay = get_random_gameplay()
# gameplay_duration = get_video_duration(gameplay)
# gameplay_section_durations = get_gameplay_duration(save_path)
# image_video = os.path.join(save_path, 'merged.mp4')
# image_video_duration = get_video_duration(image_video)

# # TODO: match video and audio length
# #get_gameplay_duration(save_path)
# #print(get_sexagesimal_time(gameplay_section_durations[0]))
# get_gameplay_section(save_path, gameplay, gameplay_section_durations[0], gameplay_section_durations[1])
# get_merged_video(save_path)