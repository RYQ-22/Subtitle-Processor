import subprocess
import re
import os
import argparse

def extract_subtitles(video_path, subtitle_path):
    # Extract subtitles from a video.
    cmd = f'ffmpeg -i "{video_path}" -map 0:s:0 "{subtitle_path}" > /dev/null 2>&1'
    subprocess.run(cmd, shell=True, check=True)

def remove_specific_lines(subtitle_path, updated_subtitle_path, patterns, line_num=50):
    # Read subtitle file and only process the first 50 lines for specified words removal.
    # Build regular expression to match any of the elements in the array
    pattern = '|'.join(re.escape(word) for word in patterns)
    with open(subtitle_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(updated_subtitle_path, 'w', encoding='utf-8') as new_file:
        # Process only the first 10 lines to check for the specified words
        for index, line in enumerate(lines):
            if index < line_num:
                if not re.search(pattern, line):
                    new_file.write(line)
            else:
                new_file.write(line)  # Write the remaining lines as they are
    
    # Delete the original subtitle file after processing
    os.remove(subtitle_path)

def add_subtitles_to_video(video_path, updated_subtitle_path, no_subtitle_video_path):
    # Remove original subtitles from the video.
    cmd = f'ffmpeg -y -i "{video_path}" -c copy -sn "{no_subtitle_video_path}" > /dev/null 2>&1'
    subprocess.run(cmd, shell=True, check=True)
    os.remove(video_path)

    # Embed the edited subtitles back into the video.
    cmd = f'ffmpeg -y -i "{no_subtitle_video_path}" -i "{updated_subtitle_path}" -c copy -c:s copy -metadata:s:s:0 language=chi -disposition:s:0 default "{video_path}" > /dev/null 2>&1'
    subprocess.run(cmd, shell=True, check=True)
    
    # Delete the updated subtitle file after embedding
    os.remove(updated_subtitle_path)
    os.remove(no_subtitle_video_path)

def process_video_subtitles(video_file, text_patterns):
    (base_name, extension_name) = video_file.rsplit('.', 1)
    subtitle_file = f"{base_name}_sub.ass"
    updated_subtitle_file = f"{base_name}_sub_new.ass"
    no_subtitle_video_file = f"{base_name}_no_sub.{extension_name}"

    extract_subtitles(video_file, subtitle_file)
    remove_specific_lines(subtitle_file, updated_subtitle_file, text_patterns)
    add_subtitles_to_video(video_file, updated_subtitle_file, no_subtitle_video_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process video files to remove specific subtitle lines.")
    parser.add_argument('-d', '--directory', required=True, help="Directory containing video files.")
    parser.add_argument('text_patterns', nargs='+', help="Text patterns to remove from subtitles.")
    
    args = parser.parse_args()

    directory = args.directory
    text_patterns = args.text_patterns

    for filename in os.listdir(directory):
        if filename.endswith('.mkv') or filename.endswith('.mp4'):
            video_path = os.path.join(directory, filename)
            print(f"Processing video: {filename}")
            process_video_subtitles(video_path, text_patterns)
    print("END")
