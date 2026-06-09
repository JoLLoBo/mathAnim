#!/usr/bin/env python3
import cv2
import numpy as np
import sys

# ============================================================
#  HARDCODED CONFIGURATION – adjust these to your needs
# ============================================================

# Input video files (order: top‑left, top‑right, bottom‑left, bottom‑right)
VIDEO_PATHS = [
    "csVideos/jiggle.mp4",
    "csVideos/jumpspot.mp4",
    "csVideos/awphold.mp4",
    "csVideos/jiggle.mp4",
]

# Output video file name
OUTPUT_FILE = "output_quadrant.mp4"

# Desired output resolution (width x height)
# Each quadrant will be exactly half of this.
OUTPUT_WIDTH = 1920
OUTPUT_HEIGHT = 1080

# Frame rate for the output video. Set to None to auto-detect
# from the first video (recommended, but you can override).
FPS = None

# Video codec (fourcc). 'mp4v' works well for .mp4 files.
FOURCC = "mp4v"

# ============================================================
#  End of configuration
# ============================================================


def main():
    # Quadrant dimensions (half of the output canvas)
    quad_width = OUTPUT_WIDTH // 2
    quad_height = OUTPUT_HEIGHT // 2

    # First pass: open each video just to get its FPS and frame count
    video_info = []
    for path in VIDEO_PATHS:
        cap = cv2.VideoCapture(path)
        if not cap.isOpened():
            print(f"ERROR: Cannot open '{path}'")
            sys.exit(1)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()
        if fps <= 0 or fps > 120:
            print(f"Warning: '{path}' has invalid FPS ({fps:.2f}), defaulting to 30.")
            fps = 30.0
        video_info.append((fps, frame_count))

    # Determine output FPS
    if FPS is None:
        output_fps = video_info[0][0]  # use first video's FPS
        print(f"Using FPS from first video: {output_fps:.2f}")
    else:
        output_fps = FPS
        print(f"Using user-defined FPS: {output_fps:.2f}")

    # Set up the video writer
    fourcc = cv2.VideoWriter_fourcc(*FOURCC)
    out = cv2.VideoWriter(
        OUTPUT_FILE, fourcc, output_fps, (OUTPUT_WIDTH, OUTPUT_HEIGHT)
    )
    if not out.isOpened():
        print("ERROR: Could not open video writer")
        sys.exit(1)

    total_written = 0  # total frames written to the output
    canvas = np.zeros((OUTPUT_HEIGHT, OUTPUT_WIDTH, 3), dtype=np.uint8)

    # Helper to place a resized frame into the correct quadrant
    def set_quadrant(frame, idx):
        if idx == 0:
            canvas[0:quad_height, 0:quad_width] = frame
        elif idx == 1:
            canvas[0:quad_height, quad_width:OUTPUT_WIDTH] = frame
        elif idx == 2:
            canvas[quad_height:OUTPUT_HEIGHT, 0:quad_width] = frame
        else:  # idx == 3
            canvas[quad_height:OUTPUT_HEIGHT, quad_width:OUTPUT_WIDTH] = frame

    # Process each video sequentially, quadrant by quadrant
    for quad_idx, (path, (video_fps, video_frames)) in enumerate(
        zip(VIDEO_PATHS, video_info)
    ):
        cap = cv2.VideoCapture(path)
        duration = video_frames / video_fps  # length of this video in seconds
        print(
            f"Processing quadrant {quad_idx+1}: '{path}' "
            f"({video_frames} frames, {video_fps:.2f} fps, {duration:.2f}s)"
        )

        # Read the very first frame
        ret, current_frame = cap.read()
        if not ret:
            print(f"  Warning: could not read first frame, quadrant stays black.")
            cap.release()
            continue

        # source_frame_end_time marks when the current source frame should be replaced
        source_frame_end_time = 1.0 / video_fps
        output_idx = 0  # how many output frames we've written for this video

        while True:
            output_time = output_idx / output_fps
            if output_time >= duration:
                break  # we've written all frames for this video's duration

            # Advance to the next source frame if it's time
            while ret and output_time >= source_frame_end_time:
                ret, new_frame = cap.read()
                if ret:
                    current_frame = new_frame
                    source_frame_end_time += 1.0 / video_fps
                # if no more frames, we keep the last valid one

            # Place the (possibly new) frame into the current quadrant
            resized = cv2.resize(current_frame, (quad_width, quad_height))
            set_quadrant(resized, quad_idx)

            out.write(canvas)
            total_written += 1
            output_idx += 1

        cap.release()
        print(f"  ... wrote {output_idx} output frames for this quadrant.")
        # The canvas now permanently holds the last frame of this video

    out.release()
    print(f"Done. Output saved as '{OUTPUT_FILE}' ({total_written} frames).")


if __name__ == "__main__":
    main()
