import argparse
import os
import cv2
import time
import platform


def parse_args():
    parser = argparse.ArgumentParser(description="Capture and store true mono video in chunks.")
    parser.add_argument("--video", type=str, help="Path to input video file.")
    parser.add_argument("--cam", type=int, help="Camera index for webcam input.")
    parser.add_argument("--fps", type=int, default=30, help="Frames per second.")
    parser.add_argument("--out", type=str, default="output.mp4", help="Base output filename (use .mp4).")
    parser.add_argument("--show", default=True, action="store_true", help="Show preview window.")
    parser.add_argument("--chunk", type=float, default=1, help="Chunk length in minutes (default=1).")
    return parser.parse_args()


def capture():
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
    CAPTURE_WIDTH = 1920
    CAPTURE_HEIGHT = 1080
    CAPTURE_FPS = args.fps
    OUTPUT_FILE = args.out
    SHOW_PREVIEW = args.show
    OUTPUT_DIR = "outputs"
    CHUNK_MINUTES = args.chunk
    CHUNK_SECONDS = CHUNK_MINUTES * 60

    # --- Prepare output directory ---
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # --- Open capture device or file ---
    if platform.system() == "Windows":
        cap = cv2.VideoCapture(INPUT)
    else: 
        cap = cv2.VideoCapture(INPUT, cv2.CAP_V4L2)

    if not cap.isOpened():
        print(f"Error: Unable to open video source {INPUT}")
        return

    # --- Configure camera properties ---
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"mp4v"))
    cap.set(cv2.CAP_PROP_FPS, CAPTURE_FPS)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAPTURE_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAPTURE_HEIGHT)

    # Tuning parameters (may vary depending on the camera driver) 
    cap.set(cv2.CAP_PROP_GAMMA, 200) 
    cap.set(cv2.CAP_PROP_GAIN, 0) 
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 0) 
    cap.set(cv2.CAP_PROP_CONTRAST, 0) 
    # cap.set(cv2.CAP_PROP_SATURATION, 0) # 0 mono, 128 color 
    # cap.set(cv2.CAP_PROP_EXPOSURE, 3) 
    # cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
    # Manual mode #cap.set(cv2.CAP_PROP_AUTO_WB, 0) # Disable auto white balance
    # cap.set(cv2.CAP_PROP_WB_TEMPERATURE, 4500)
    # cap.set(cv2.CAP_PROP_AUTOFOCUS, 0) # Disable autofocus
    # cap.set(cv2.CAP_PROP_FOCUS, 0) 
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 10)

    # --- Verify final configuration ---
    WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    FPS = int(cap.get(cv2.CAP_PROP_FPS))
    GAMMA = int(cap.get(cv2.CAP_PROP_GAMMA))

    print(f"Platform: {platform.system()}")
    print(f"WxH: {WIDTH}x{HEIGHT}")
    print(f"FPS: {FPS}")
    print(f"Gamma: {GAMMA}")

    # --- Setup video writer (chunk-based) ---
    chunk_index = 1
    def get_output_path(index):
        base, ext = os.path.splitext(OUTPUT_FILE)
        return os.path.join(OUTPUT_DIR, f"{base}_{index:03d}{ext}")

    output_path = get_output_path(chunk_index)
    writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"mp4v"), CAPTURE_FPS, (WIDTH, HEIGHT))

    # --- Tracking time ---
    chunk_start_time = time.time()

    # --- Capture loop ---
    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video or failed to grab frame.")
            break

        # Save frame to current chunk
        writer.write(frame)

        # Show preview if enabled
        if SHOW_PREVIEW:
            cv2.imshow("Press 'q' to quit", frame)

        # Check if chunk duration exceeded
        elapsed = time.time() - chunk_start_time
        if elapsed >= CHUNK_SECONDS:
            # Close current file
            writer.release()
            print(f"Chunk saved: {output_path}")

            # Start new chunk
            chunk_index += 1
            output_path = get_output_path(chunk_index)
            writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"mp4v"), CAPTURE_FPS, (WIDTH, HEIGHT))
            chunk_start_time = time.time()

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("Exit requested by user.")
            break

    # --- Cleanup ---
    cap.release()
    writer.release()
    cv2.destroyAllWindows()
    print("Capture finished.")


if __name__ == "__main__":
    capture()
