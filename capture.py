"""
Capture and store true mono video from either a webcam or a video file.

This script allows you to:
- Capture video from a connected camera or read from a video file.
- Save the captured video to disk in `.mp4` format.
- Optionally preview the captured video in real time.
- Configure camera properties (exposure, gamma, focus, etc.).

Dependencies:
    - OpenCV (cv2)
    - NumPy
    - argparse
    - os
"""

import argparse
import os
import cv2
import numpy as np


def parse_args():
    """
    Parse command-line arguments for configuring video capture.

    Returns:
        argparse.Namespace: Parsed arguments with the following attributes:
            --video (str): Path to input video file.
            --cam (int): Camera index for webcam input.
            --fps (int): Frames per second (default=30).
            --out (str): Output filename (default="output.mp4").
            --show (bool): Show preview window if set.
    """
    parser = argparse.ArgumentParser(description="Capture and store true mono video.")
    parser.add_argument("--video", type=str, help="Path to input video file.")
    parser.add_argument("--cam", type=int, help="Camera index for webcam input.")
    parser.add_argument("--fps", type=int, default=30, help="Frames per second.")
    parser.add_argument("--out", type=str, default="output.mp4", help="Output filename (use .mp4).")
    parser.add_argument("--show", default=True, action="store_true", help="Show preview window.")
    return parser.parse_args()


def capture():
    """
    Main function to handle video capture, configuration, and saving.

    Steps:
        1. Parse input arguments (video file or camera index).
        2. Configure capture properties (resolution, FPS, exposure, etc.).
        3. Open input source (video file or camera).
        4. Capture frames in a loop until user quits or source ends.
        5. Save output video in the `outputs/` directory.
    """
    args = parse_args()

    # --- Select input source ---
    if args.video:
        INPUT = args.video
    elif args.cam is not None:
        INPUT = args.cam
    else:
        print("Error: You must specify either --video or --cam.")
        return

    # --- Configuration ---
    CAPTURE_WIDTH = 1280
    CAPTURE_HEIGHT = 800
    CAPTURE_FPS = args.fps
    OUTPUT_FILE = args.out
    SHOW_PREVIEW = args.show
    OUTPUT_DIR = "outputs"

    # --- Prepare output directory ---
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    OUTPUT_FILE_PATH = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

    # --- Open capture device or file ---
    cap = cv2.VideoCapture(INPUT, cv2.CAP_V4L2)  # Use V4L2 backend (Linux-specific)
    if not cap.isOpened():
        print(f"Error: Unable to open video source {INPUT}")
        return

    # --- Configure camera properties ---
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))  # Set codec
    cap.set(cv2.CAP_PROP_FPS, CAPTURE_FPS)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAPTURE_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAPTURE_HEIGHT)

    # Tuning parameters (may vary depending on the camera driver)
    cap.set(cv2.CAP_PROP_GAMMA, 200)
    cap.set(cv2.CAP_PROP_GAIN, 0)
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 0)
    cap.set(cv2.CAP_PROP_CONTRAST, 0)
    #cap.set(cv2.CAP_PROP_SATURATION, 0) # 0 mono, 128 color
    #cap.set(cv2.CAP_PROP_EXPOSURE, 3)
    #cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # Manual mode
    #cap.set(cv2.CAP_PROP_AUTO_WB, 0)  # Disable auto white balance
    #cap.set(cv2.CAP_PROP_WB_TEMPERATURE, 4500)
    #cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)  # Disable autofocus
    #cap.set(cv2.CAP_PROP_FOCUS, 0)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 10)

    # --- Verify final configuration ---
    WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    FPS = int(cap.get(cv2.CAP_PROP_FPS))

    print(f"WxH: {WIDTH}x{HEIGHT}")
    print(f"FPS: {FPS}")
    print(f"Gamma: {cap.get(cv2.CAP_PROP_GAMMA):.1f}")

    # --- Setup video writer ---
    writer = cv2.VideoWriter(OUTPUT_FILE_PATH, cv2.VideoWriter_fourcc(*"MJPG"), FPS, (WIDTH, HEIGHT))

    # --- Capture loop ---
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame.")
            break

        # Save frame to output file
        writer.write(frame)

        # Show preview if enabled
        if SHOW_PREVIEW:
            cv2.imshow("Press 'q' to quit", frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("Exit requested by user.")
            break

    # --- Cleanup ---
    cap.release()
    writer.release()
    cv2.destroyAllWindows()
    print(f"Output video saved at {OUTPUT_FILE_PATH}")


if __name__ == "__main__":
    capture()
