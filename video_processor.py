# frame_extractor.py
import os
import cv2

def extract_frames(input_path, output_path, filename_video, timestamp):
    # Create the output directory if it doesn't exist
    output_frame_dir = output_frame_dir + '/' + timestamp

    os.makedirs(output_frame_dir, exist_ok=True)

    # Open the video file
    cap = cv2.VideoCapture(input_path + filename_video)

    # Get the frames per second (FPS) of the video
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    print(f'video fps: {fps}')

    frame_count = 0  # Initialize frame count

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Output every second frame (skip two out of every three frames)
        if frame_count % 3 == 0:
            # Save the frame as an image
            frame_filename = os.path.join(output_frame_dir, f'frame_{frame_count // 3:04d}.jpg')
            cv2.imwrite(frame_filename, frame)

        frame_count += 1
    # Release the video capture
    cap.release()
