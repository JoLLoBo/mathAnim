#!/usr/bin/env python3
import cv2
import numpy as np
import subprocess
import sys

VIDEO_PATHS = [
    "csVideos/jiggle.mp4",
    "csVideos/jumpspot.mp4",
    "csVideos/pixel.mp4",
    "csVideos/awphold.mp4",
]

OUTPUT_FILE = "output_quadrant.mp4"

W, H = 1920, 1080
QW, QH = W // 2, H // 2
FPS = 60

# Slow motion factor: 2 = half speed, 3 = one third speed, etc.
SLOW_FACTOR = 2


def open_caps():
    caps = []
    for p in VIDEO_PATHS:
        cap = cv2.VideoCapture(p)
        if not cap.isOpened():
            print("Cannot open", p)
            sys.exit(1)
        caps.append(cap)
    return caps


def main():
    caps = open_caps()

    # Read first frame from each video to initialise current frames
    current_frames = []
    for cap in caps:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read first frame from a video")
            sys.exit(1)
        frame = cv2.resize(frame, (QW, QH))
        current_frames.append(frame)

    ffmpeg = [
        "ffmpeg",
        "-y",
        "-f",
        "rawvideo",
        "-vcodec",
        "rawvideo",
        "-pix_fmt",
        "bgr24",
        "-s",
        f"{W}x{H}",
        "-r",
        str(FPS),
        "-i",
        "-",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        OUTPUT_FILE,
    ]

    proc = subprocess.Popen(ffmpeg, stdin=subprocess.PIPE)

    while True:
        # Write the current frame set SLOW_FACTOR times
        for _ in range(SLOW_FACTOR):
            canvas = np.zeros((H, W, 3), dtype=np.uint8)
            for i, frame in enumerate(current_frames):
                y, x = (i // 2) * QH, (i % 2) * QW
                canvas[y : y + QH, x : x + QW] = frame
            proc.stdin.write(canvas.tobytes())

        # Read new frames from all videos (update only those that have more data)
        any_alive = False
        for i, cap in enumerate(caps):
            ret, frame = cap.read()
            if ret:
                any_alive = True
                current_frames[i] = cv2.resize(frame, (QW, QH))
            # else: keep the previous frame (video ended)

        if not any_alive:
            break

    # Cleanup
    for c in caps:
        c.release()
    proc.stdin.close()
    proc.wait()
    print("Done:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
