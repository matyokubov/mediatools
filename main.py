import ffmpeg
import pysubs2
import os

def extract_subtitles(input_file, subtitle_file, language="eng"):
    """Extract the English subtitle from the MKV file"""
    ffmpeg.input(input_file).output(subtitle_file, map='0:s:0').run()

def shift_subtitle_and_following(subtitle_file, original_start_time, new_start_time):
    """Shift the specific subtitle and all following by the calculated duration"""
    subs = pysubs2.load(subtitle_file)
    
    # Convert times to milliseconds
    original_start_time_ms = original_start_time * 1000
    new_start_time_ms = new_start_time * 1000
    shift_duration = new_start_time_ms - original_start_time_ms

    # Find the first subtitle at 07:59 and adjust it, along with all following
    for line in subs:
        if line.start >= original_start_time_ms:
            line.shift(ms=shift_duration)

    subs.save(subtitle_file)

def merge_subtitles_back(input_file, subtitle_file, output_file):
    """Merge the adjusted subtitle track back into the MKV file"""
    os.system(f'mkvmerge -o "{output_file}" --subtitle-tracks 0 "{input_file}" --no-video --no-audio "{subtitle_file}"')

# Define file paths
input_file = '01 The God Delusion.mkv'
subtitle_file = 'english_subtitles.srt'
output_file = 'output_movie_fixed_subtitles.mkv'

# Step 1: Extract the English subtitles
extract_subtitles(input_file, subtitle_file)

# Step 2: Shift the subtitle starting at 07:59 to start at 08:13 and adjust all following subtitles
original_start_time = 7 * 60 + 59  # 07:59 in seconds
new_start_time = 8 * 60 + 13       # 08:13 in seconds

# Shift the specific subtitle and all subsequent ones
shift_subtitle_and_following(subtitle_file, original_start_time, new_start_time)

# Step 3: Merge the adjusted subtitle track back into the MKV file
merge_subtitles_back(input_file, subtitle_file, output_file)

print(f"Subtitles adjusted and saved to {output_file}")

