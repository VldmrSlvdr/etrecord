# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   @File Name:     main_set.py
   @Author:        Yifei LI
   @Date:          2024/05/01
   @Description:
-------------------------------------------------
"""

import os
import pandas as pd
from data_processor import DataProcessor
from video_processor import VideoProcessor
from data_integrator import DataIntegrator

class ExperimentProcessor:
    def __init__(self, config):
        self.config = config

    def process_all_participants(self):
        """Process all participants defined in the configuration."""
        for participant in self.config['participants']:
            self.process_participant(participant)

    def process_participant(self, participant):
        """Process data for a single participant and combine data across sessions."""
        combined_exp_data = []
        combined_gaze_data = []
        combined_rating_data = []
        combined_integ_data = []  # Initialize a list to store rating data from all sessions

        output_path = os.path.join(participant['output_path'])
        if not os.path.exists(output_path):
            os.makedirs(output_path, exist_ok=True)

        for session in participant['sessions']:
            session_config = {
                'base_path': os.path.join(participant['base_path']),
                'output_path': participant['output_path'],
                'exp_file': session['exp_file'],
                'gaze_file': session['gaze_file'],
                'video_file': session['video_file'],
                'position_file': session['position_file']  # Assume there's a position file defined
            }
            data_processor = DataProcessor(session_config)  # Initialize DataProcessor with session config

            # Process the experimental file
            exp_data = data_processor.select_columns()  # Direct call to select_columns
            if exp_data is not None:
                exp_data.to_csv(os.path.join(session_config['output_path'], f"{session['id']}_exp.csv"), index=False)
                combined_exp_data.append(exp_data)

            # Extract the rating data
            rating_data = data_processor.extract_rating_data()
            if rating_data is not None:
                combined_rating_data.append(rating_data)

            # Process the gaze file
            gaze_data = data_processor.process_data()  # Assuming this processes and merges gaze data
            if gaze_data is not None:
                combined_gaze_data.append(gaze_data)

            # Process the video file
            video_file = os.path.join(session_config['base_path'], session_config['video_file'])
            video_processor = VideoProcessor(session_config)  # Initialize VideoProcessor with session config
            video_data = video_processor.process_video_and_detect_areas()  # Direct call to process video
            if video_data is not None:
                video_frame = pd.DataFrame(video_data)
                video_frame.to_csv(os.path.join(session_config['output_path'], f"{session['id']}_video_analysis.csv"), index=False)
            
            # Integrate the multiple data files 
            data_integrator = DataIntegrator(session_config) 
            integ_data = data_integrator.integrate_data()
            if integ_data is not None:
                integ_data.to_csv(os.path.join(session_config['output_path'], f"{session['id']}_integ.csv"), index=False)
                combined_integ_data.append(integ_data)

        # After processing all sessions, combine and save experimental and gaze data
        if combined_exp_data:
            all_exp_data = pd.concat(combined_exp_data, ignore_index=True)
            all_exp_data.to_csv(os.path.join(participant['output_path'], f"{participant['participant_id']}_combined_exp_data.csv"), index=False)
        
        if combined_gaze_data:
            all_gaze_data = pd.concat(combined_gaze_data, ignore_index=True)
            all_gaze_data.to_csv(os.path.join(participant['output_path'], f"{participant['participant_id']}_combined_gaze_data.csv"), index=False)

        if combined_rating_data:
            all_rating_data = pd.concat(combined_rating_data, ignore_index=True)
            all_rating_data.to_csv(os.path.join(participant['output_path'], f"{participant['participant_id']}_rating_data.csv"), index=False)
        
        if combined_integ_data:
            all_integ_data = pd.concat(combined_integ_data, ignore_index=True)
            all_integ_data.to_csv(os.path.join(participant['output_path'], f"{participant['participant_id']}_integ_data.csv"), index=False)


def main():
    import yaml
    with open('config_sets.yaml', 'r') as f:
        config = yaml.safe_load(f)
    processor = ExperimentProcessor(config)
    processor.process_all_participants()

if __name__ == '__main__':
    main()
