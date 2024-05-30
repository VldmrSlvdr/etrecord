# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   @File Name:     process_video.py
   @Author:        Yifei LI
   @Date:          2024/05/30
   @Description:
-------------------------------------------------
"""
import os
import cv2
import yaml
import pandas as pd
from app.video_processor import VideoProcessor
from app.data_processor import DataProcessor

def visualize_interest_areas(config):
    """
    Visualize interest areas frame by frame for each participant's video and record data in a CSV file.
    """
    for participant in config['participants']:
        for session in participant['sessions']:
            video_config = {
                'base_path': participant['base_path'],
                'output_path': participant['output_path'],
                'video_file': session['video_file']
            }
            data_config = {
                'base_path': participant['base_path'],
                'output_path': participant['output_path'],
                'exp_file': session['exp_file'],
                'gaze_file': session['gaze_file']
            }
            processor = VideoProcessor(video_config)
            data_processor = DataProcessor(data_config)
            gaze_data = data_processor.load_gaze_data()
            visualize_and_record_video(processor, gaze_data, session['id'], participant['output_path'])

def visualize_and_record_video(processor, gaze_data, session_id, output_path):
    """
    Process and display the video with detected and inferred interest areas,
    visualize gaze data, and record the data in a CSV file.
    """
    # Open the video file
    cap = cv2.VideoCapture(os.path.join(processor.input_path, processor.filename_video))
    fps = cap.get(cv2.CAP_PROP_FPS)  # Get the frames per second of the video

    # Initialize frame count and prepare output data
    frame_count = 0
    output_data = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Calculate elapsed time in milliseconds
        elapsed_time_ms = (frame_count / fps) * 1000

        # Determine the trial number and phase based on the elapsed time
        trial_num = int(elapsed_time_ms // 6000) + 1
        trial_phase = (elapsed_time_ms % 6000) // 1000
        if trial_phase == 0:
            trial_phase_name = 'fixation'
        elif trial_phase == 1:
            trial_phase_name = 'arrow'
        elif 2 <= trial_phase <= 4:
            trial_phase_name = 'figures'
        else:
            trial_phase_name = 'blank'

        # Detect interest areas in the current frame
        interest_areas = processor.detect_interest_areas(frame, frame_count)

        # Infer the third area
        third_area = processor.infer_third_area(
            frame_count,
            interest_areas[0] if len(interest_areas) > 0 else None,
            interest_areas[1] if len(interest_areas) > 1 else None
        )

        # Prepare area info for recording
        area_info = {
            'interest_area_1': interest_areas[0] if len(interest_areas) > 0 else None,
            'interest_area_2': interest_areas[1] if len(interest_areas) > 1 else None,
            'interest_area_3': third_area
        }

        # Overlay the detected and inferred areas on the frame
        for area in interest_areas:
            _, x, y, w, h = area
            start_point = (int(x * frame.shape[1]), int(y * frame.shape[0]))
            end_point = (int((x + w) * frame.shape[1]), int((y + h) * frame.shape[0]))
            color = (0, 255, 0)  # Green color for rectangles
            thickness = 2
            cv2.rectangle(frame, start_point, end_point, color, thickness)

        if third_area is not None:
            _, x, y, w, h = third_area
            start_point = (int(x * frame.shape[1]), int(y * frame.shape[0]))
            end_point = (int((x + w) * frame.shape[1]), int((y + h) * frame.shape[0]))
            color = (0, 0, 255)  # Red color for the inferred area
            thickness = 2
            cv2.rectangle(frame, start_point, end_point, color, thickness)

        # Visualize gaze data and check if gaze position is in any interest area
        in_area = False
        left_or_right = ''
        if frame_count < len(gaze_data):
            norm_x = gaze_data.iloc[frame_count]['norm_pos_x']
            norm_y = gaze_data.iloc[frame_count]['norm_pos_y']
            gaze_point = (int(norm_x * frame.shape[1]), int((1 - norm_y) * frame.shape[0]))  # Note: norm_y is inverted
            cv2.circle(frame, gaze_point, 5, (255, 0, 0), -1)  # Blue color for gaze points

            for area in interest_areas:
                _, x, y, w, h = area
                if x <= norm_x <= x + w and y <= norm_y <= y + h:
                    in_area = True
                    cv2.circle(frame, gaze_point, 5, (0, 255, 255), -1)  # Yellow color if within an interest area

            # Determine if gaze position is on the left or right side of the screen
            left_or_right = 'left' if norm_x < 0.5 else 'right'

        # Overlay trial number and phase on the frame
        text = f'Trial: {trial_num}, Phase: {trial_phase_name}'
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Record the data
        output_data.append({
            'session': session_id,
            'frame': frame_count,
            'elapsed_time_ms': elapsed_time_ms,
            'trial_num': trial_num,
            'trial_phase': trial_phase_name,
            'gaze_position': (norm_x, norm_y) if frame_count < len(gaze_data) else None,
            'area_info': area_info,
            'in_area': in_area,
            'left_or_right': left_or_right
        })

        # Display the frame
        cv2.imshow('Frame with Interest Areas and Gaze Points', frame)

        # Press 'q' to exit the video display
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

        frame_count += 1

    # Release the video capture
    cap.release()
    cv2.destroyAllWindows()

    # Save the output data to a CSV file
    output_df = pd.DataFrame(output_data)
    output_csv_path = os.path.join(output_path, f'session_{session_id}_output.csv')
    output_df.to_csv(output_csv_path, index=False)

if __name__ == "__main__":
    # Specify the path to your YAML configuration file
    yaml_file_path = 'config_sets.yaml'

    # Load the YAML configuration from the file
    with open(yaml_file_path, 'r') as file:
        config = yaml.safe_load(file)

    # Visualize interest areas and gaze points based on the configuration
    visualize_interest_areas(config)
