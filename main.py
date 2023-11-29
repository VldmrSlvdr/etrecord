# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   @File Name:     main.py
   @Author:        Yifei LI
   @Date:          2023/11/01
   @Description:
-------------------------------------------------
"""
import os
import yaml
import pandas as pd
import argparse

from data_processor import DataProcessor
from video_processor import VideoProcessor
from data_integrator import DataIntegrator

# from video_processor import VideoProcessor
class ExperimentProcessor:
    def __init__(self, config):
        self.input_path = config["input_path"]
        self.output_path = config["output_path"]
        self.filename_exp = config["filename_exp"]
        self.filename_gaze = config["filename_gaze"]
        self.filename_position = config["filename_position"]
        self.filename_video = config["filename_video"]
        self.data_processor = DataProcessor(config)
        self.video_processor = VideoProcessor(config)
        self.data_integrator = DataIntegrator(config)

    # def process(self):
        # Process data using DataProcessor
        # self.data_processor.process_data()
        # interest_areas = self.video_processor.process_video_and_detect_areas()
        # AOI = pd.DataFrame(interest_areas)
        # AOI.to_csv(self.output_path + 'AOI.csv')

        # exposure = self.data_processor.select_columns()
        # rating = self.data_processor.extract_rating_data()

        
        # Placeholder for video processing (uncomment if VideoProcessor is implemented)
        # self.video_processor.detect_interest_areas()

        # Placeholder for integrating results and converting to CSV
        # self.data_integrator.integrate_data()
        # self.save_results()

    def save_results(self):

        # exposure.to_csv(self.output_path + 'exposure.csv')
        # rating.to_csv(self.output_path + 'rating.csv')

        # Implement the logic to save the results, possibly using the visualizer module
        pass

    def process_files_only(self, input_folder):
        """
        Process each CSV file in the input_folder, extract participant_id, and save the processed file 
        in the output_folder with a filename that includes the participant_id.
        """
        exposure_frames = []
        rating_frames = []

        for root, dirs, files in os.walk(input_folder):
            for file in files:
                if file.endswith('.csv'):
                    file_path = os.path.join(root, file)
                    print(f"Processing file: {file_path}")
                    print(f"root: {root}")
                    print(f"file: {file}")
                    self.data_processor.input_path = root + '/'
                    self.data_processor.filename_exp = file  # Update other filenames as needed

                    # Process the data using DataProcessor
                    data_exposure = self.data_processor.select_columns() 

                    if data_exposure is not None and not data_exposure.empty:
                        # Extract participant_id
                        participant_id = data_exposure['participant'].iloc[3]
                        session_id = data_exposure['session'].iloc[3]
                        participant_id_str = str(int(participant_id))
                        session_id_str = str(int(session_id))

                        # Save the processed data
                        output_dir = root.replace(input_folder, self.output_path)
                        os.makedirs(output_dir, exist_ok=True)
                        output_file_path = os.path.join(output_dir, f"{participant_id_str}_{session_id_str}_exposure.csv")
                        data_exposure.to_csv(output_file_path, index=False)
                        exposure_frames.append(data_exposure)
                    
                    data_rating = self.data_processor.extract_rating_data()

                    if data_rating is not None and not data_rating.empty:
                        output_dir = root.replace(input_folder, self.output_path)
                        os.makedirs(output_dir, exist_ok=True)
                        output_file_path = os.path.join(output_dir, f"{participant_id_str}_{session_id_str}_rating.csv")
                        data_rating.to_csv(output_file_path, index=False)
                        rating_frames.append(data_rating)
        
        # Concatenate and save all exposure data
        if exposure_frames:
            all_exposure = pd.concat(exposure_frames)
            all_exposure['show'] = True
            all_exposure.to_csv(os.path.join(self.output_path, 'exposure_all.csv'), index=False)

        # Concatenate and save all rating data
        if rating_frames:
            all_rating = pd.concat(rating_frames)
            all_rating.to_csv(os.path.join(self.output_path, 'rating_all.csv'), index=False)
        
        # Merge exposure and rating data
        # df_select_exposure = all_exposure[['participant','target_image','show']]
        # df_merged = pd.merge(all_rating, df_select_exposure, on=['participant', 'target_image'])
        # df_merged.to_csv(os.path.join(self.output_path, 'merged_all.csv'), index=True)

    def process_files_all(self, input_folder):
        """
        Process each CSV file in the input_folder, extract participant_id, and save the processed file 
        in the output_folder with a filename that includes the participant_id.
        """
        exposure_frames = []
        rating_frames = []

        for root, dirs, files in os.walk(input_folder):
            for file in files:
                if file.endswith('.csv') and 'eye20' in file:
                    file_path = os.path.join(root, file)
                    print(f"Processing file: {file_path}")
                    print(f"root: {root}")
                    print(f"file: {file}")
                    self.data_processor.input_path = root + '/'
                    self.data_processor.filename_exp = file  # Update other filenames as needed

                    # Process the data using DataProcessor
                    data_exposure = self.data_processor.select_columns() 

                    if data_exposure is not None and not data_exposure.empty:
                        # Extract participant_id
                        participant_id = data_exposure['participant'].iloc[3]
                        session_id = data_exposure['session'].iloc[3]
                        participant_id_str = str(int(participant_id))
                        session_id_str = str(int(session_id))

                        # Save the processed data
                        output_dir = root.replace(input_folder, self.output_path)
                        os.makedirs(output_dir, exist_ok=True)
                        output_file_path = os.path.join(output_dir, f"{participant_id_str}_{session_id_str}_exposure.csv")
                        data_exposure.to_csv(output_file_path, index=False)
                        exposure_frames.append(data_exposure)
                    
                    data_rating = self.data_processor.extract_rating_data()

                    if data_rating is not None and not data_rating.empty:
                        output_dir = root.replace(input_folder, self.output_path)
                        os.makedirs(output_dir, exist_ok=True)
                        output_file_path = os.path.join(output_dir, f"{participant_id_str}_rating.csv")
                        data_rating.to_csv(output_file_path, index=False)
                        rating_frames.append(data_rating)
                
                elif file.endswith('world.mp4'):
                    file_path = os.path.join(root, file)
                    print(f"Processing file: {file_path}")
                    print(f"root: {root}")
                    print(f"file: {file}")
                    self.data_processor.input_path = root + '/'
                    self.data_processor.filename_video = file  # Update other filenames as needed

                    # process video data 
                    interest_areas = self.video_processor.process_video_and_detect_areas()
                    data_aoi = pd.DataFrame(interest_areas)

                    if data_aoi is not None and not data_aoi.empty:
                        # Save the processed data
                        output_dir = root.replace(input_folder, self.output_path)
                        os.makedirs(output_dir, exist_ok=True)
                        output_file_path = os.path.join(output_dir, f"{participant_id_str}_aoi.csv")

                        data_aoi.to_csv(output_file_path, index=False)

        # Concatenate and save all exposure data
        if exposure_frames:
            all_exposure = pd.concat(exposure_frames)
            all_exposure['show'] = True
            all_exposure.to_csv(os.path.join(self.output_path, 'exposure_all.csv'), index=False)

        # Concatenate and save all rating data
        if rating_frames:
            all_rating = pd.concat(rating_frames)
            all_rating.to_csv(os.path.join(self.output_path, 'rating_all.csv'), index=False)

    def process_gaze_data(self, input_folder):
        """
        Process gaze data from a CSV file and save the processed data in the output folder.
        """
        for root, dirs, files in os.walk(input_folder):
            # Initialize variables to store the loaded data for each subdirectory
            loaded_data_exp = None
            loaded_data_gaze = None

            for file in files:
                if file.endswith('.csv') and 'eye20' in file:
                    file_path = os.path.join(root, file)
                    print(f"Processing file: {file_path}")
                    print(f"root: {root}")
                    print(f"file: {file}")
                    self.data_processor.input_path = root + '/'
                    self.data_processor.filename_exp = file  # Update other filenames as needed

                if file.endswith('gaze_positions.csv'):
                    file_path = os.path.join(root, file)
                    print(f"Processing file: {file_path}")
                    print(f"root: {root}")
                    print(f"file: {file}")
                    self.data_processor.input_path = root + '/'
                    self.data_processor.filename_gaze = file  # Update other filenames as needed

                

                    # Process the data using DataProcessor
                    data_gaze = self.data_processor.process_data()

                    if data_gaze is not None and not data_gaze.empty:
                        # Save the processed data
                        output_dir = root.replace(input_folder, self.output_path)
                        os.makedirs(output_dir, exist_ok=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='Path to the config file')
    parser.add_argument('--mode', help='Mode to run the script', default='test')

    args = parser.parse_args()

    # Load config here
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    # config = load_config(args.config)
    experiment_processor = ExperimentProcessor(config)

    if args.mode == 'data_process_only':
        experiment_processor.process_files_only(config["input_dir"])
    elif args.mode == 'test':
        experiment_processor.process()
    elif args.mode == 'process_all':
        experiment_processor.process_files_all(config["input_dir"])
        experiment_processor.merge_data(config["output_path"])

if __name__ == '__main__':
    main()