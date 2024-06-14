import moviepy.editor as mp
import pysrt
from datetime import timedelta
import subprocess
import chardet

def time_to_timedelta(t):
    h, m, s = map(int, t.split(':'))
    return timedelta(hours=h, minutes=m, seconds=s)

def timedelta_to_subriptime(td):
    total_seconds = int(td.total_seconds())
    milliseconds = int(td.microseconds / 1000)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return pysrt.SubRipTime(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    return result['encoding']
    
def cut_video(input_path, output_path, start_time, end_time):
    try:
        video = mp.VideoFileClip(input_path)
        start_time = time_to_timedelta(start_time).total_seconds()
        end_time = time_to_timedelta(end_time).total_seconds()
        cut_video = video.subclip(start_time, end_time)
        cut_video.write_videofile(output_path, codec='libx264', audio_codec='aac')
        print(f"Video cut successfully and saved to {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def cut_subtitles(input_path, output_path, start_time, end_time):
    """
    Cuts a section from an SRT subtitle file.
    
    :param input_path: Path to the input SRT file.
    :param output_path: Path where the output SRT file will be saved.
    :param start_time: Start time in 'HH:MM:SS' format.
    :param end_time: End time in 'HH:MM:SS' format.
    """
    try:
        # Detect the encoding of the input subtitle file
        encoding = detect_encoding(input_path)
        
        # Load the subtitles with the detected encoding
        subs = pysrt.open(input_path, encoding=encoding)
        
        # Convert start and end times to timedelta
        start_time_td = time_to_timedelta(start_time)
        end_time_td = time_to_timedelta(end_time)
        
        # Filter and adjust subtitles within the specified time range
        new_subs = pysrt.SubRipFile()
        for sub in subs:
            sub_start_td = timedelta(hours=sub.start.hours, minutes=sub.start.minutes, seconds=sub.start.seconds, milliseconds=sub.start.milliseconds)
            sub_end_td = timedelta(hours=sub.end.hours, minutes=sub.end.minutes, seconds=sub.end.seconds, milliseconds=sub.end.milliseconds)
            if start_time_td <= sub_start_td <= end_time_td:
                # Adjust the subtitle timing to be relative to the new start time
                new_start_td = sub_start_td - start_time_td
                new_end_td = sub_end_td - start_time_td
                sub.start = timedelta_to_subriptime(new_start_td)
                sub.end = timedelta_to_subriptime(new_end_td)
                new_subs.append(sub)
        
        # Save the result
        new_subs.save(output_path, encoding='utf-8')
        
        print(f"Subtitles cut successfully and saved to {output_path}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

def combine_video_subtitles(video_path, subtitle_path, output_path):
    try:
        command = [
            'ffmpeg',
            '-i', video_path,
            '-vf', f"subtitles={subtitle_path}",
            '-c:a', 'copy',
            output_path
        ]
        subprocess.run(command, check=True)
        print(f"Video and subtitles combined successfully and saved to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

# Example usage
input_video_path = "Despicable Me.mp4"
input_subtitle_path = "Despicable Me.srt"
cut_video_path = "cut_video.mp4"
cut_subtitle_path = "cut_subtitles.srt"
final_output_path = "final_output.mp4"
start_time = "00:56:46"  # Start at 1 minute
end_time = "00:58:08"    # End at 2 minutes

# Step 1: Cut the video
cut_video(input_video_path, cut_video_path, start_time, end_time)

# Step 2: Cut the subtitles
cut_subtitles(input_subtitle_path, cut_subtitle_path, start_time, end_time)

# Step 3: Combine video and subtitles
combine_video_subtitles(cut_video_path, cut_subtitle_path, final_output_path)
