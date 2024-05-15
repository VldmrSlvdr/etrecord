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
import logging
from data_processor import DataProcessor
from video_processor import VideoProcessor
from data_integrator import DataIntegrator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ExperimentProcessor:
    def __init__(self, config):
        self.config = config

    def process_all_participants(self):
        for participant in self.config['participants']:
            self.process_participant(participant)

    def process_participant(self, participant):
        logging.info(f"Processing participant {participant['participant_id']}")
        combined_exp_data, combined_gaze_data, combined_rating_data, combined_integ_data = [], [], [], []

        for session in participant['sessions']:
            try:
                self.process_session(participant, session)
            except Exception as e:
                logging.error(f"Error processing session {session['id']} for participant {participant['participant_id']}: {e}")
                continue

        self.save_combined_data(participant['output_path'], participant['participant_id'], 
                                combined_exp_data, combined_gaze_data, combined_rating_data, combined_integ_data)

    def ensure_directory_exists(directory):
        """Ensure the directory exists, and if not, create it."""
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

    def process_session(self, participant, session):

        session_config = self.build_session_config(participant, session)
        data_processor = DataProcessor(session_config)
        video_processor = VideoProcessor(session_config)
        data_integrator = DataIntegrator(session_config)
        if not os.path.exists(session_config['output_path']):
            os.makedirs(session_config['output_path'], exist_ok=True)

        exp_data, gaze_data, video_data = self.handle_data_processing(data_processor, video_processor, session_config, session)
        if gaze_data is not None and video_data is not None:
            self.integrate_and_save_data(gaze_data, video_data, data_integrator, session_config, session)

    def handle_data_processing(self, data_processor, video_processor,session_config, session):
        exp_data = data_processor.select_columns()
        gaze_data = data_processor.process_data()
        video_data = video_processor.process_video_and_detect_areas()

            # Ensure gaze_data is a DataFrame
        if isinstance(gaze_data, list):  # Check if the data is a list and convert if necessary
            gaze_data = pd.DataFrame(gaze_data)
        elif gaze_data is None:
            print("Gaze data is None, skipping sorting and further processing for gaze data.")
        else:
            # Ensure the gaze_data is sorted if it's already a DataFrame
            gaze_data = gaze_data.sort_values('gaze_stamp') if 'gaze_stamp' in gaze_data.columns else gaze_data

        video_data = video_processor.process_video_and_detect_areas()
        
        # Ensure video_data is a DataFrame
        if isinstance(video_data, list):  # Check if the data is a list and convert if necessary
            video_data = pd.DataFrame(video_data)
        elif video_data is None:
            print("Video data is None, skipping further processing for video data.")
        else:
            # Add any specific handling for video_data if it's already a DataFrame
            pass

        if exp_data is not None:
            exp_data.to_csv(os.path.join(session_config['output_path'], f"{session['id']}_exp.csv"), index=False)
        if gaze_data is not None:
            gaze_data.to_csv(os.path.join(session_config['output_path'], f"{session['id']}_gaze.csv"), index=False)
        if video_data is not None:
            pd.DataFrame(video_data).to_csv(os.path.join(session_config['output_path'], f"{session['id']}_video_analysis.csv"), index=False)
        return exp_data, gaze_data, video_data

    def integrate_and_save_data(self, gaze_data, video_data, data_integrator, session_config, session):
        integ_data = data_integrator.integrate_data(gaze_data, video_data)
        if integ_data is not None:
            integ_data.to_csv(os.path.join(session_config['output_path'], f"{session['id']}_integ.csv"), index=False)

    def save_combined_data(self, output_path, participant_id, exp_data, gaze_data, rating_data, integ_data):
        if not os.path.exists(output_path):
            os.makedirs(output_path, exist_ok=True)

        if exp_data:
            pd.concat(exp_data, ignore_index=True).to_csv(os.path.join(output_path, f"{participant_id}_combined_exp_data.csv"), index=False)
        if gaze_data:
            pd.concat(gaze_data, ignore_index=True).to_csv(os.path.join(output_path, f"{participant_id}_combined_gaze_data.csv"), index=False)
        if rating_data:
            pd.concat(rating_data, ignore_index=True).to_csv(os.path.join(output_path, f"{participant_id}_rating_data.csv"), index=False)
        if integ_data:
            pd.concat(integ_data, ignore_index=True).to_csv(os.path.join(output_path, f"{participant_id}_integ_data.csv"), index=False)

    def build_session_config(self, participant, session):
        return {
            'base_path': os.path.join(participant['base_path']),
            'output_path': participant['output_path'],
            'exp_file': session['exp_file'],
            'gaze_file': session['gaze_file'],
            'video_file': session['video_file']
        }

def main():
    import yaml
    with open('config_sets.yaml', 'r') as f:
        config = yaml.safe_load(f)
    processor = ExperimentProcessor(config)
    processor.process_all_participants()

if __name__ == '__main__':
    main()
