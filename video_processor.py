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

                # Calculate the third area
                third_area = self.infer_third_area(frame_count, 
                    interest_areas[0] if len(interest_areas) > 0 else None,
                    interest_areas[1] if len(interest_areas) > 1 else None
                )

                # Include the third area in the frame data
                frame_data['interest_area_3'] = third_area
                frames_and_areas.append(frame_data)
    
            frame_count += 1

        # Release the video capture
        cap.release()

        return frames_and_areas

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
        
    def infer_third_area(self, frame_count, area1, area2):
        """
        Infers the coordinates of a third interest area based on the first two detected areas.
        The third area lies below areas 1 and 2, its height is 20% of the mean height of the first two areas,
        and its width is 1.5 times the total width of the first two areas.
        """
        if area1 is None or area2 is None:
            return None

        _, x1, y1, w1, h1 = area1
        _, x2, y2, w2, h2 = area2

        # Calculate the mean height of areas 1 and 2
        mean_height = (h1 + h2) / 2

        # Calculate the total width of areas 1 and 2
        total_width = w1 + w2

        # Calculate the position and size of the third area
        x3 = min(x1, x2) - 0.1
        y3 = max(y1 + h1, y2 + h2)  # Position it below the lower of the two areas
        w3 = 1.5 * total_width
        h3 = 0.2 * mean_height

        return (frame_count, x3, y3, w3, h3)