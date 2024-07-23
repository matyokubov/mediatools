import subprocess
import os

def extract_mp3_from_mkv(input_mkv_path, output_mp3_path):
    try:
        # Check if ffmpeg is installed
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Run the ffmpeg command to extract mp3 from mkv
        command = [
            "ffmpeg",
            "-i", input_mkv_path,   # Input MKV file
            "-vn",                  # Disable video recording
            "-acodec", "libmp3lame", # Use MP3 codec
            output_mp3_path         # Output MP3 file
        ]
        subprocess.run(command, check=True)
        print(f"MP3 extracted successfully to {output_mp3_path}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while extracting MP3: {e}")
    except FileNotFoundError:
        print("ffmpeg is not installed. Please install it and try again.")

# Example usage:
input_mkv = "Black_Widow_XXX_An_Axel_Braun_Parody_2021.mkv"
output_mp3 = "Black_Widow_XXX_An_Axel_Braun_Parody_2021.mp3"

extract_mp3_from_mkv(input_mkv, output_mp3)
