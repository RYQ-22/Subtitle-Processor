# Subtitle-Processor
Process video files to remove specific subtitle lines according to the input text patterns.
根据输入的关键词自动匹配，去除对应行的字幕。

In this script, only first 50 lines of the subtitle file will be processed. You can edit it as you want.
在这个脚本只有字幕文件的前50行会被处理。如有需要，可以自行修改。

## Usage
```
python subtitle_processor.py -d /path/to/directory text_pattern1 text_pattern2 ... 
```

Make sure `ffmpeg` is installed on you system.
