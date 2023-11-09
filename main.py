# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   @File Name:     main.py
   @Author:        Yifei LI
   @Date:          2023/11/01
   @Description:
-------------------------------------------------
"""
import yaml
import pandas as pd
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

    def process(self):
        # Process data using DataProcessor
        # self.data_processor.process_data()
        # interest_areas = self.video_processor.process_video_and_detect_areas()
        # AOI = pd.DataFrame(interest_areas)
        # AOI.to_csv(self.output_path + 'AOI.csv')

        # exposure = self.data_processor.select_columns()
        # rating = self.data_processor.extract_rating_data()

        
        # Placeholder for video processing (uncomment if VideoProcessor is implemented)
        # self.video_processor.detect_interest_areas()
        self.data_integrator.filter_data()

        # Placeholder for integrating results and converting to CSV
        # self.save_results()

    def save_results(self):

        # exposure.to_csv(self.output_path + 'exposure.csv')
        # rating.to_csv(self.output_path + 'rating.csv')

        # Implement the logic to save the results, possibly using the visualizer module
        pass

def main(config):
    processor = ExperimentProcessor(config)
    processor.process()

if __name__ == "__main__":
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    main(config)