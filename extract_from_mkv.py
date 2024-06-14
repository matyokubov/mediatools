import subprocess
import os

def extract_from_mkv(mkv_file, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract video stream to MP4
    mp4_output = os.path.join(output_dir, "output.mp4")
    subprocess.run(['ffmpeg', '-i', mkv_file, '-codec', 'copy', mp4_output], check=True)
    print(f"Extracted video to {mp4_output}")
    
    # Extract subtitle streams to SRT
    # First, get the subtitle stream info
    result = subprocess.run(['ffmpeg', '-i', mkv_file], stderr=subprocess.PIPE, universal_newlines=True)
    output = result.stderr

    # Find the subtitle streams in the output
    subtitle_streams = []
    for line in output.split('\n'):
        if 'Subtitle:' in line:
            subtitle_streams.append(line)
    
    if not subtitle_streams:
        print("No subtitle streams found.")
        return
    
    for idx, stream in enumerate(subtitle_streams):
        # Extract the stream index number
        stream_index = stream.split()[0].split('[')[-1].split(']')[0]
        
        # Define output filename
        srt_output = os.path.join(output_dir, f"output_{idx}.srt")
        
        # Extract subtitle stream
        subprocess.run(['ffmpeg', '-i', mkv_file, '-map', f'0:{stream_index}', srt_output], check=True)
        print(f"Extracted subtitle stream {idx} to {srt_output}")

# Example usage
extract_from_mkv('Despicable Me.mkv', './')
