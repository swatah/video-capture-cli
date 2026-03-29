# Video Capture CLI Tool

A simple Python command-line tool for capturing video from a file or webcam using OpenCV.

## Features

- Accepts video file input via `--video` or webcam input via `--cam`.
- Allows setting capture FPS with `--fps` (default: 30).
- Saves output to a specified video file using `--out` (default: `output.mp4`).
- Option to show preview during capture with `--show` (default: `True`).
- Automatically creates an `output` directory to save the video file.

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

### Capture from webcam

```bash
python capture.py --cam 0 --fps 30 --out output.mp4 --show True
```

### Capture from video file

```bash
python capture.py --video input.mp4 --fps 30 --out output.mp4 --show True
```

### Options:

- --video: Path to input video file (either .mp4, .avi, etc.)

- --cam: Camera index for webcam input (e.g., 0, 1, etc.)

- --fps: Frames per second for output video (default: 30).

- --out: Output video filename (default: output.mp4).

- --show: Whether to show preview during capture (True or False, default: True).

### Example:

```bash
python capture.py --cam 0 --fps 25 --out capture_output.mp4 --show True
```

This will capture from the first webcam, at 25 FPS, and save the output to capture_output.mp4 with preview.

### Notes

- .mp4 is used as the default output format. Ensure that FFmpeg is properly configured for OpenCV to write .mp4 files.

- Press q to stop the capture and close the preview window.
