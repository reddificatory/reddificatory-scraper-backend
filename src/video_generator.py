import subprocess
import os
import glob
import random
import audio
import uuid

def merge_images(save_path):
    current_directory = os.getcwd()
    save_path = os.path.join(current_directory, save_path)
    os.chdir(save_path)
    os.system(f'ffmpeg -f concat -i images.txt -c png merged.mp4')
    os.chdir(current_directory)

def run(save_path):
    merge_images(save_path)

    background_path = os.path.join(os.getcwd(), 'media', 'background')
    background_video = get_background_video(background_path)
    background_video_duration = get_duration(background_path, background_video)
    overlay_video = 'merged.mp4'
    # get audio duration instead of video duartion since it's incorrect for some reason
    # TODO: fix video durations
    # overlay_video_duration = get_duration(save_path, overlay_video)
    overlay_video_duration = audio.get_duration(os.path.join(save_path, 'merged.wav'))
    start_end_times = get_random_start_end_times(background_video_duration, overlay_video_duration)

    get_video_section(background_path, background_video, save_path, start_end_times[0], start_end_times[1])
    merge_final_video(save_path)

def get_duration(path, file_name):
    current_directory = os.getcwd()
    path = os.path.join(current_directory, path)
    os.chdir(path)
    duration = float(subprocess.check_output(f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{file_name}"').decode())
    os.chdir(current_directory)

    return duration

# TODO: check if background is longer than or equal to the overlay length
def get_background_video(path):
    current_directory = os.getcwd()
    path = os.path.join(current_directory, path)
    os.chdir(path)
    videos = glob.glob('*.webm')
    random_index = random.randint(0, len(videos) - 1)
    os.chdir(current_directory)

    return videos[random_index]

def get_sexagesimal_time(seconds):
    total_seconds, fractional_seconds = divmod(seconds, 1)
    hours, remaining_seconds = divmod(int(total_seconds), 3600)
    minutes, seconds = divmod(remaining_seconds, 60)
    sexagesimal_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{int(fractional_seconds * 1000):03d}"
    return sexagesimal_time

def get_random_start_end_times(duration1, duration2):
    if duration1 < duration2:
        temp_duration = duration1
        duration1 = duration2
        duration2 = temp_duration

    random_start_time = random.uniform(0, duration1) - 1
    random_end_time = random_start_time + duration2

    while random_end_time > duration1:
        random_start_time = random.uniform(0, duration1) - 1
        random_end_time = random_start_time + duration2

    return random_start_time, random_end_time

def get_video_section(file_path, file_name, save_path, start_time, end_time):
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, file_path)
    os.chdir(file_path)
    output_uuid = uuid.uuid4()

    command = f'ffmpeg -ss {get_sexagesimal_time(start_time)} -to {get_sexagesimal_time(end_time)} -i "{file_name}" -filter_complex "[0:v]crop=ih*(9/16):ih[cropped]" -map [cropped] {output_uuid}.mp4'    
    os.system(command)
    os.rename(os.path.join(file_path, f'{output_uuid}.mp4'), os.path.join(save_path, 'background.mp4'))

    os.chdir(current_directory)

def merge_final_video(save_path):    
    current_directory = os.getcwd()
    save_path = os.path.join(current_directory, save_path)
    os.chdir(save_path)

    command = f'ffmpeg -i background.mp4 -i merged.mp4 -i merged.wav -filter_complex "[1:v][0:v]scale2ref=iw*0.9:ow/mdar[ovrl][backgr];[backgr][ovrl]overlay=(W-w)/2:(H-h)/2[outv]" -map [outv] -map 2:a video.mp4'
    os.system(command)

    os.chdir(current_directory)