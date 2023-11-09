# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   @File Name:     video_processor.py
   @Author:        Yifei LI
   @Date:          2023/11/01
   @Description:
-------------------------------------------------
"""
import os
import cv2
import numpy as np

class VideoProcessor:
    def __init__(self, config):
        """
        Initialize the VideoProcessor with file paths and filenames from the given configuration.
        """
        self.input_path = config['input_path']
        self.output_path = config['output_path']
        self.filename_video = config['filename_video']

    def process_video_and_detect_areas(self):
        # Open the video file
        cap = cv2.VideoCapture(os.path.join(self.input_path, self.filename_video))
        fps = cap.get(cv2.CAP_PROP_FPS)  # Get the frames per second of the video

        # Initialize frame count
        frame_count = 0
        frames_and_areas = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Calculate elapsed time in seconds
            elapsed_time = frame_count / fps

            # Skip two out of every three frames
            if frame_count % 1 == 0:
                # Detect interest areas in the current frame
                interest_areas = self.detect_interest_areas(frame, frame_count)

                # Compile the frame and interest areas into a data structure
                frame_data = {
                    'count': frame_count,
                    'elapsed_time': elapsed_time,
                    'interest_area_1': interest_areas[0] if len(interest_areas) > 0 else None,
                    'interest_area_2': interest_areas[1] if len(interest_areas) > 1 else None
                }
                frames_and_areas.append(frame_data)

            frame_count += 1

        # Release the video capture
        cap.release()

        return frames_and_areas

    def detect_stimulus(self):
        """
        Detect a stimulus in a video and return relevant information.
        """
        # Placeholder function body
        return None

    def detect_interest_areas(self, frame, frame_count):
            """
            Analyze a video frame to detect areas of interest based on color thresholds and geometric criteria.
            Returns a list of normalized interest areas (x, y, width, height) as ratios of the frame size.
            """
            try:
                hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                # Define your color range for detection
                lower_color = np.array([0, 0, 0])  # Example: Change to your specifics
                upper_color = np.array([180, 180, 180])  # Example: Change to your specifics

                # Detect areas of interest
                color_mask = cv2.inRange(hsv_image, lower_color, upper_color)
                less_interested_mask = cv2.bitwise_not(color_mask)
                contours, _ = cv2.findContours(less_interested_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                interested_rectangles_centered_and_ranged = []
                image_center_x = frame.shape[1] / 2
                image_center_y = frame.shape[0] / 2
                center_threshold = 0.4 * min(frame.shape[1], frame.shape[0])
                y_range_min = 0.2 * frame.shape[0]
                y_range_max = 0.8 * frame.shape[0]

                for contour in contours:
                    x, y, w, h = cv2.boundingRect(contour)
                    rect_center_x = x + w / 2
                    rect_center_y = y + h / 2
                    distance_to_center = np.sqrt((rect_center_x - image_center_x) ** 2 + (rect_center_y - image_center_y) ** 2)

                    if distance_to_center <= center_threshold and y + h >= y_range_min and y + h <= y_range_max:
                        # Normalize the coordinates
                        normalized_x = x / frame.shape[1]
                        normalized_y = y / frame.shape[0]
                        normalized_w = w / frame.shape[1]
                        normalized_h = h / frame.shape[0]
                        interested_rectangles_centered_and_ranged.append((frame_count, normalized_x, normalized_y, normalized_w, normalized_h))

                # Sort the rectangles by width in descending order and keep the top 2
                top_2_widest_rectangles = sorted(interested_rectangles_centered_and_ranged, key=lambda rect: rect[3], reverse=True)[:2]

                return top_2_widest_rectangles

            except Exception as e:
                print(f"Error while detecting interest areas: {e}")
                return []