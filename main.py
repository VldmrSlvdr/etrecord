# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   @File Name:     main.py
   @Author:        Yifei LI
   @Date:          2023/11/01
   @Description:
-------------------------------------------------
"""
import yaml, os
from data_processor import *
from video_processor import *
from visualizer import *
from utils import *

def main(config):
    def __init__(self, input_dir, output_dir):
        # load config files
        with open('config/config.yaml', 'r') as config_file:
            config = yaml.safe_load(config_file)
        
        self.input_path = config['input_path']
        self.output_path = config['output_path']
        self.filename_exp = config['filename_exp']
        self.filename_gaze = config['filename_gaze']
        self.filename_position = config['filename_position']
        self.time_interval = config['time_interval']
        self.filename_video = config['filename_video']
    
    # import the critical functions for further data reshape
    data_processer = DataProcessor()
    video_processer = VideoProcessor()
    
    # reshape data 
    data_processer.process_data()

    # process video and return the results of stimulus delection
    video_processer.detect_interest_areas()


    # integrate the results and convert it into 

if __name__ == '__main__':
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    main(config)