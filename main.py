import datetime, yaml
from data_reshape import *
from video_processor import *
from utils import *

if __name__ == '__main__':
    # load config files
    with open('config/config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)

    input_path = config['input_path']
    output_path = config['output_path']
    filename_exp = config['filename_exp']
    filename_gaze = config['filename_gaze']
    filename_position = config['filename_position']
    time_interval = config['time_interval']
    filename_video = config['filename_video']

    # add a timestamp 
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # Process data
    processor = DataProcessor(input_path, output_path)
    processor.process_data(filename_exp, filename_gaze, filename_position, time_interval)

    # Extract frames
    extract_frames(input_path, output_path, filename_video, timestamp)

    # Detect Stimulus

    # Integrate data for outputs
