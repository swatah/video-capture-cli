import argparse
import os
import cv2


def parse_args():
    parser = argparse.ArgumentParser(description="Capture and process video input.")
    parser.add_argument("--video", type=str, help="Path to input video file.")
    parser.add_argument("--cam", type=int, help="Camera index for webcam input.")
    parser.add_argument(
        "--fps", type=int, default=30, help="Frames per second for output video."
    )
    parser.add_argument(
        "--out", type=str, default="output.mp4", help="Output video filename."
    )
    parser.add_argument("--show", type=bool, default=True, help="Show preview.")
    return parser.parse_args()


def capture():
    args = parse_args()

    if args.video:
        INPUT_CAM = args.video
    elif args.cam is not None:
        INPUT_CAM = args.cam
    else:
        print("Error: You must specify either --video or --cam.")
        return

    CAPTURE_FPS = args.fps
    OUTPUT_FILE = args.out
    SHOW_PREVIEW = args.show
    OUTPUT_DIR = "output"

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    cap = cv2.VideoCapture(INPUT_CAM)
    cap.set(cv2.CAP_PROP_FPS, CAPTURE_FPS)

    WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    OUTPUT_FILE_PATH = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    out = cv2.VideoWriter(
        OUTPUT_FILE_PATH, cv2.VideoWriter_fourcc(*"mp4v"), CAPTURE_FPS, (WIDTH, HEIGHT)
    )

    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"video/cam fps:{fps:.0f} FPS, output fps:{CAPTURE_FPS}")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame.")
            break

        out.write(frame)

        if SHOW_PREVIEW:
            cv2.imshow("Capture - Press 'q' to quit", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("Exit requested by user.")
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Output video saved at {OUTPUT_FILE_PATH}")


if __name__ == "__main__":
    capture()
