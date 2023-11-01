# frame_extractor.py
import os, cv2
import numpy as np

class VideoProcessor:
    def extract_frames(input_path, output_path, filename_video, timestamp):
        # Create the output directory if it doesn't exist
        output_frame_dir = output_path + '/' + timestamp

        os.makedirs(output_frame_dir, exist_ok=True)

        # Open the video file
        cap = cv2.VideoCapture(input_path + filename_video)

        # Get the frames per second (FPS) of the video
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        # print(f'video fps: {fps}')

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

    def detect_stimulus(input_path, output_path, timestamp):
        x = 1
        return x

    def detect_interest_areas(frame, frame_count):
        hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_color = np.array([0, 0, 0])  # Adjust these values based on your specific color
        upper_color = np.array([180, 180, 180])  # Adjust these values based on your specific color

        color_mask = cv2.inRange(hsv_image, lower_color, upper_color)
        less_interested_mask = cv2.bitwise_not(color_mask)

        contours, _ = cv2.findContours(less_interested_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        interested_rectangles_centered_and_ranged = []
        image_center_x = frame.shape[1] // 2
        image_center_y = frame.shape[0] // 2
        center_threshold = 0.4
        y_range_min = 0.2
        y_range_max = 0.8

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            rect_center_x = x + w // 2
            rect_center_y = y + h // 2

            distance_to_center = np.sqrt((rect_center_x - image_center_x) ** 2 + (rect_center_y - image_center_y) ** 2)

            if (
                distance_to_center <= center_threshold * min(frame.shape[0], frame.shape[1]) and
                y_range_min <= (y + h) / frame.shape[0] <= y_range_max
            ):
                interested_rectangles_centered_and_ranged.append((frame_count, x, y, w, h))

        # Sort the rectangles by width in descending order
        sorted_rectangles = sorted(interested_rectangles_centered_and_ranged, key=lambda rect: rect[2], reverse=True)

        # Keep the top 2 widest rectangles
        top_2_widest_rectangles = sorted_rectangles[:2]

        return top_2_widest_rectangles