import argparse
import os
import cv2

def parse_args():
    p = argparse.ArgumentParser(description="Capture and process video input.")
    p.add_argument("--video", type=str, help="Path to input video file.")
    p.add_argument("--cam", type=int, help="Camera index for webcam input.")
    p.add_argument("--fps", type=int, default=120, help="Output FPS.")
    p.add_argument("--out", type=str, default="output.avi", help="Output filename.")
    p.add_argument("--show", action="store_true", help="Show preview window.")
    return p.parse_args()

def capture():
    args = parse_args()

    if not args.video and args.cam is None:
        print("Error: You must specify either --video or --cam.")
        return

    OUTPUT_DIR = "outputs"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    OUTPUT_FILE_PATH = os.path.join(OUTPUT_DIR, args.out)

    # Pick sensible backend
    if args.video:
        cap = cv2.VideoCapture(args.video, cv2.CAP_FFMPEG)
    else:
        cap = cv2.VideoCapture(args.cam, cv2.CAP_V4L2)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
        cap.set(cv2.CAP_PROP_FPS, args.fps)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)
        cap.set(cv2.CAP_PROP_GAMMA, 200)

    if not cap.isOpened():
        print("Error: Failed to open input.")
        return

    # Read one frame to lock actual size
    ret, frame = cap.read()
    if not ret or frame is None:
        print("Error: Could not read first frame.")
        return

    height, width = frame.shape[:2]
    input_fps = cap.get(cv2.CAP_PROP_FPS) or 0
    print(f"Detected input fps: {input_fps:.0f} | Output fps: {args.fps}")
    print(f"Resolution: {width} x {height}")

    # OPTION A: keep MJPG in color (convert gray back to BGR before write)
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    out = cv2.VideoWriter(OUTPUT_FILE_PATH, fourcc, args.fps, (width, height))
    if not out.isOpened():
        print(f"Error: Failed to open VideoWriter for {OUTPUT_FILE_PATH}")
        return

    # Write the first frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)  # ensure 3 channels for MJPG
    out.write(bgr)
    if args.show:
        cv2.imshow("Capture - Press 'q' to quit", cv2.resize(gray, (1024, 720)))

    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            print("End of stream or failed to grab frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        out.write(bgr)

        if args.show:
            cv2.imshow("Capture - Press 'q' to quit", cv2.resize(gray, (1024, 720)))
            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("Exit requested by user.")
                break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Output video saved at {OUTPUT_FILE_PATH}")

if __name__ == "__main__":
    capture()
